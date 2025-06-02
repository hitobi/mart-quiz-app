import sys
import cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                           QScrollArea, QFrame, QListWidget, QSplitter)
from PyQt5.QtGui import QPixmap, QImage, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt
from skimage.metrics import structural_similarity as ssim
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.font_manager as fm

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

class DragDropListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event: QDropEvent):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
        
        for file_path in files:
            if any(file_path.lower().endswith(ext) for ext in valid_extensions):
                self.parent().parent().parent().add_comparison_image(file_path)

class ImageSimilarityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("이미지 유사도 검사 프로그램")
        self.setGeometry(100, 100, 1500, 900)
        
        # 메인 위젯과 레이아웃 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # 왼쪽 패널 (기준 이미지)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # 기준 이미지 레이블
        self.reference_label = QLabel("기준 이미지를 선택하세요\n(이미지를 여기에 끌어다 놓을 수 있습니다)")
        self.reference_label.setAlignment(Qt.AlignCenter)
        self.reference_label.setMinimumSize(400, 400)
        self.reference_label.setFrameStyle(QFrame.Box)
        self.reference_label.setAcceptDrops(True)
        self.reference_label.dragEnterEvent = self.reference_dragEnterEvent
        self.reference_label.dropEvent = self.reference_dropEvent
        left_layout.addWidget(self.reference_label)
        
        select_ref_btn = QPushButton("기준 이미지 선택")
        select_ref_btn.clicked.connect(self.select_reference_image)
        left_layout.addWidget(select_ref_btn)
        
        # 오른쪽 패널 (비교 이미지들과 그래프)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # 이미지 리스트와 그래프를 위한 스플리터
        splitter = QSplitter(Qt.Vertical)
        
        # 이미지 리스트 위젯
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        
        # 드래그 앤 드롭을 지원하는 리스트 위젯으로 교체
        self.image_list = DragDropListWidget()
        self.image_list.setMinimumWidth(400)
        list_layout.addWidget(QLabel("여기에 이미지를 끌어다 놓거나 아래 버튼을 클릭하세요"))
        list_layout.addWidget(self.image_list)
        
        button_layout = QHBoxLayout()
        add_images_btn = QPushButton("여러 비교 이미지 추가 (클릭 또는 드래그)")
        add_images_btn.clicked.connect(self.add_comparison_images)
        compare_btn = QPushButton("유사도 검사")
        compare_btn.clicked.connect(self.compare_images)
        clear_btn = QPushButton("목록 지우기")
        clear_btn.clicked.connect(self.clear_images)
        
        button_layout.addWidget(add_images_btn)
        button_layout.addWidget(compare_btn)
        button_layout.addWidget(clear_btn)
        list_layout.addLayout(button_layout)
        
        # 그래프를 위한 matplotlib Figure
        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        
        # 스플리터에 위젯 추가
        splitter.addWidget(list_widget)
        splitter.addWidget(self.canvas)
        right_layout.addWidget(splitter)
        
        # 메인 레이아웃에 패널 추가
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        
        # 이미지 저장을 위한 변수들
        self.reference_image_path = None
        self.comparison_image_paths = []
        self.comparison_results = []

    def reference_dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def reference_dropEvent(self, event: QDropEvent):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            self.select_reference_image(files[0])

    def select_reference_image(self, file_path=None):
        if file_path is None:
            file_path, _ = QFileDialog.getOpenFileName(self, "기준 이미지 선택", "", 
                                                     "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.reference_image_path = file_path
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.reference_label.setPixmap(scaled_pixmap)
            self.reference_label.setToolTip(file_path)

    def add_comparison_image(self, file_path):
        if file_path not in self.comparison_image_paths:
            self.comparison_image_paths.append(file_path)
            filename = file_path.split('/')[-1]
            self.image_list.addItem(filename)

    def add_comparison_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "비교할 이미지 선택", "",
                                              "Images (*.png *.jpg *.jpeg *.bmp)")
        for file_path in files:
            self.add_comparison_image(file_path)

    def clear_images(self):
        self.image_list.clear()
        self.comparison_image_paths = []
        self.comparison_results = []
        self.figure.clear()
        self.canvas.draw()

    def get_center_region(self, image, center_percentage=0.8):
        """이미지의 중앙 영역을 추출합니다."""
        height, width = image.shape
        
        # 중앙 영역의 크기 계산 (80%)
        center_height = int(height * center_percentage)
        center_width = int(width * center_percentage)
        
        # 시작점 계산 (중앙에서 시작)
        start_y = (height - center_height) // 2
        start_x = (width - center_width) // 2
        
        # 중앙 영역 추출
        center_region = image[start_y:start_y + center_height, 
                            start_x:start_x + center_width]
        
        return center_region

    def compare_images(self):
        if not self.reference_image_path:
            self.image_list.clear()
            self.image_list.addItem("❌ 기준 이미지를 선택해주세요.")
            return
        
        if not self.comparison_image_paths:
            self.image_list.clear()
            self.image_list.addItem("❌ 비교할 이미지를 추가해주세요.")
            return

        # 기준 이미지 로드
        ref_img = cv2.imread(self.reference_image_path, cv2.IMREAD_GRAYSCALE)
        if ref_img is None:
            self.image_list.clear()
            self.image_list.addItem("❌ 기준 이미지를 불러올 수 없습니다.")
            return
            
        # 기준 이미지의 중앙 80% 영역 추출
        ref_center = self.get_center_region(ref_img)
        
        self.image_list.clear()
        self.comparison_results = []
        filenames = []
        scores = []
        
        for img_path in self.comparison_image_paths:
            comp_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            
            if comp_img is None:
                self.image_list.addItem(f"❌ {img_path}: 이미지를 불러올 수 없습니다.")
                continue
                
            # 이미지 크기 맞추기
            comp_img = cv2.resize(comp_img, (ref_img.shape[1], ref_img.shape[0]))
            
            # 비교 이미지의 중앙 80% 영역 추출
            comp_center = self.get_center_region(comp_img)
            
            # SSIM 계산 (중앙 영역만)
            score, _ = ssim(ref_center, comp_center, full=True)
            
            # 결과 저장
            filename = img_path.split('/')[-1]
            filenames.append(filename)
            scores.append(score)
            
            # 리스트에 결과 표시
            self.image_list.addItem(f"📊 {filename}: 유사도 {score:.4f} (중앙 80% 영역)")
        
        # 그래프 업데이트
        if scores:
            self.plot_results(filenames, scores)

    def plot_results(self, filenames, scores):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # 막대 그래프 생성
        bars = ax.bar(range(len(scores)), scores)
        
        # x축 레이블 설정
        ax.set_xticks(range(len(filenames)))
        ax.set_xticklabels(filenames, rotation=45, ha='right')
        
        # y축 범위 설정 (0~1)
        ax.set_ylim(0, 1)
        
        # 그래프 제목과 레이블 설정
        ax.set_title('이미지 유사도 비교 결과 (중앙 80% 영역)')
        ax.set_ylabel('유사도 (SSIM)')
        
        # 각 막대 위에 값 표시
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{score:.4f}',
                   ha='center', va='bottom')
        
        # 그래프 레이아웃 조정
        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageSimilarityApp()
    window.show()
    sys.exit(app.exec_()) 