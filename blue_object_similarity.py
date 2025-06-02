import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                           QScrollArea, QFrame, QListWidget, QSplitter, QSlider,
                           QListWidgetItem)
from PyQt5.QtGui import QPixmap, QImage, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import platform

# 한글 폰트 설정
if platform.system() == 'Darwin':  # macOS
    plt.rc('font', family='AppleGothic')
else:  # Windows
    plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

class BlueObjectDetector:
    def __init__(self):
        # HSV 색공간에서 파란색 범위 설정
        self.lower_blue = np.array([100, 50, 50])
        self.upper_blue = np.array([130, 255, 255])
        
    def detect_blue_object(self, image):
        # BGR to HSV 변환
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # 파란색 마스크 생성
        mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue)
        
        # 노이즈 제거
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # 윤곽선 찾기
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None, None
        
        # 가장 큰 윤곽선 선택
        largest_contour = max(contours, key=cv2.contourArea)
        
        # 마스크와 윤곽선 반환
        result_mask = np.zeros_like(mask)
        cv2.drawContours(result_mask, [largest_contour], -1, (255), -1)
        
        return result_mask, largest_contour

    def compare_shapes(self, contour1, contour2):
        if contour1 is None or contour2 is None:
            return 0.0
        
        # 윤곽선 매칭
        similarity = cv2.matchShapes(contour1, contour2, cv2.CONTOURS_MATCH_I2, 0.0)
        # matchShapes는 값이 작을수록 유사, 값의 범위를 0~1로 변환
        similarity = 1 / (1 + similarity)
        return similarity

class DraggableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.InternalMove)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dragEnterEvent(self, event):
        mime = event.mimeData()
        if mime.hasUrls() or mime.hasText():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            
            valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
            for file_path in links:
                if any(file_path.lower().endswith(ext) for ext in valid_extensions):
                    # 상위 위젯의 메서드 호출
                    window = self.window()
                    if isinstance(window, ImageSimilarityApp):
                        window.add_comparison_image(file_path)
        else:
            super().dropEvent(event)

class ImageSimilarityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("파란색 물체 형태 유사도 검사 프로그램")
        self.setGeometry(100, 100, 1500, 900)
        
        self.detector = BlueObjectDetector()
        
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
        
        # 기준 이미지의 파란색 물체 표시 레이블
        self.reference_blue_label = QLabel("파란색 물체 검출 결과")
        self.reference_blue_label.setAlignment(Qt.AlignCenter)
        self.reference_blue_label.setMinimumSize(400, 400)
        self.reference_blue_label.setFrameStyle(QFrame.Box)
        left_layout.addWidget(self.reference_blue_label)
        
        select_ref_btn = QPushButton("기준 이미지 선택")
        select_ref_btn.clicked.connect(lambda: self.select_reference_image())
        left_layout.addWidget(select_ref_btn)
        
        # 오른쪽 패널
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # 이미지 리스트와 그래프를 위한 스플리터
        splitter = QSplitter(Qt.Vertical)
        
        # 이미지 리스트 위젯
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        
        # 드래그 앤 드롭 안내 메시지
        drop_label = QLabel("")
        drop_label.setAlignment(Qt.AlignCenter)
        list_layout.addWidget(drop_label)
        
        # 드래그 가능한 리스트 위젯
        self.image_list = DraggableListWidget()
        self.image_list.setMinimumWidth(400)
        self.image_list.setMinimumHeight(200)
        self.image_list.itemSelectionChanged.connect(self.update_comparison_paths)
        list_layout.addWidget(self.image_list)
        
        button_layout = QHBoxLayout()
        add_images_btn = QPushButton("여러 비교 이미지 추가")
        add_images_btn.clicked.connect(self.add_comparison_images)
        
        compare_btn = QPushButton("형태 유사도 검사")
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
        self.reference_contour = None
        self.comparison_image_paths = []
        self.path_to_item = {}  # 파일 경로와 리스트 아이템 매핑

    def update_comparison_paths(self):
        """리스트 위젯의 순서 변경을 comparison_image_paths에 반영"""
        new_paths = []
        for i in range(self.image_list.count()):
            item = self.image_list.item(i)
            path = item.data(Qt.UserRole)  # 저장된 전체 경로 가져오기
            new_paths.append(path)
        self.comparison_image_paths = new_paths

    def reference_dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def reference_dropEvent(self, event: QDropEvent):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            self.select_reference_image(files[0])

    def convert_cv_to_pixmap(self, cv_img):
        height, width = cv_img.shape[:2]
        if len(cv_img.shape) == 2:  # 그레이스케일 이미지
            qimg = QImage(cv_img.data, width, height, width, QImage.Format_Grayscale8)
        else:  # BGR 이미지
            bytes_per_line = 3 * width
            qimg = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        return QPixmap.fromImage(qimg)

    def select_reference_image(self, file_path=None):
        if file_path is None:
            file_path, _ = QFileDialog.getOpenFileName(self, "기준 이미지 선택", "", 
                                                     "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.reference_image_path = file_path
            # 원본 이미지 표시
            img = cv2.imread(file_path)
            if img is None:
                self.reference_label.setText("이미지를 불러올 수 없습니다.")
                return
                
            pixmap = self.convert_cv_to_pixmap(img)
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.reference_label.setPixmap(scaled_pixmap)
            
            # 파란색 물체 검출
            mask, contour = self.detector.detect_blue_object(img)
            if mask is None:
                self.reference_blue_label.setText("파란색 물체를 찾을 수 없습니다.")
                self.reference_contour = None
                return
                
            self.reference_contour = contour
            
            # 마스크 이미지 표시
            mask_pixmap = self.convert_cv_to_pixmap(mask)
            scaled_mask_pixmap = mask_pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.reference_blue_label.setPixmap(scaled_mask_pixmap)

    def add_comparison_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "비교할 이미지 선택", "",
                                              "Images (*.png *.jpg *.jpeg *.bmp)")
        for file_path in files:
            if file_path not in self.comparison_image_paths:
                self.comparison_image_paths.append(file_path)
                filename = file_path.split('/')[-1]
                item = QListWidgetItem(filename)
                item.setData(Qt.UserRole, file_path)  # 전체 경로 저장
                self.image_list.addItem(item)
                self.path_to_item[file_path] = item

    def clear_images(self):
        self.image_list.clear()
        self.comparison_image_paths = []
        self.path_to_item = {}
        self.figure.clear()
        self.canvas.draw()

    def compare_images(self):
        if not self.reference_image_path or self.reference_contour is None:
            self.image_list.clear()
            self.image_list.addItem("기준 이미지의 파란색 물체를 찾을 수 없습니다.")
            return
        
        if not self.comparison_image_paths:
            self.image_list.addItem("비교할 이미지를 추가해주세요.")
            return

        results = []  # 결과를 저장할 리스트
        
        for img_path in self.comparison_image_paths:
            img = cv2.imread(img_path)
            if img is None:
                item = QListWidgetItem(f"{img_path.split('/')[-1]}: 이미지를 불러올 수 없습니다.")
                item.setForeground(Qt.red)
                self.image_list.addItem(item)
                continue
            
            # 파란색 물체 검출
            mask, contour = self.detector.detect_blue_object(img)
            if mask is None:
                item = QListWidgetItem(f"{img_path.split('/')[-1]}: 파란색 물체를 찾을 수 없습니다.")
                item.setForeground(Qt.red)
                self.image_list.addItem(item)
                continue
            
            # 형태 유사도 계산
            score = self.detector.compare_shapes(self.reference_contour, contour)
            
            # 결과 저장
            filename = img_path.split('/')[-1]
            results.append((filename, score))
            
            # 리스트에 결과 표시
            item = QListWidgetItem(f"{filename}: 형태 유사도 {score:.4f}")
            item.setData(Qt.UserRole, img_path)
            self.image_list.addItem(item)
        
        # 그래프 업데이트
        if results:
            filenames, scores = zip(*results)
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
        ax.set_title('파란색 물체 형태 유사도 비교 결과')
        ax.set_ylabel('형태 유사도')
        
        # 각 막대 위에 값 표시
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{score:.4f}',
                   ha='center', va='bottom')
        
        # 그래프 레이아웃 조정
        self.figure.tight_layout()
        self.canvas.draw()

    def add_comparison_image(self, file_path):
        """단일 이미지를 비교 목록에 추가"""
        if file_path not in self.comparison_image_paths:
            self.comparison_image_paths.append(file_path)
            filename = file_path.split('/')[-1]
            item = QListWidgetItem(filename)
            item.setData(Qt.UserRole, file_path)  # 전체 경로 저장
            self.image_list.addItem(item)
            self.path_to_item[file_path] = item
            return True
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageSimilarityApp()
    window.show()
    sys.exit(app.exec_()) 