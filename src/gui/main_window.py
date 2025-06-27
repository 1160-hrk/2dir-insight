"""
main_window.py - メインGUIウィンドウ

2dir-insightのメインアプリケーションウィンドウ
"""

import sys
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QMenuBar, QStatusBar, QToolBar, QSplitter,
    QFileDialog, QMessageBox, QAction, QLabel
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QKeySequence

# プロジェクト内のモジュールインポート
try:
    from .spectrum_viewer import SpectrumViewer
    from .controls import ParameterControls
    from .dialogs import SettingsDialog, AboutDialog
    from ..core.data_loader import DataLoader
except ImportError:
    # 開発中の場合のフォールバック
    pass


class MainWindow(QMainWindow):
    """メインアプリケーションウィンドウ"""
    
    # シグナル定義
    data_loaded = pyqtSignal(dict)
    settings_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        
        # データ管理
        self.data_loader = DataLoader()
        self.current_data = None
        self.settings = {}
        
        # UI初期化
        self.init_ui()
        self.load_settings()
        
        # 状態管理
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)  # 1秒毎に更新
    
    def init_ui(self):
        """ユーザーインターフェースを初期化"""
        self.setWindowTitle("2dir-insight - 2次元NMRスペクトロスコピー学習システム")
        self.setGeometry(100, 100, 1200, 800)
        
        # メニューバー作成
        self.create_menu_bar()
        
        # ツールバー作成
        self.create_toolbar()
        
        # ステータスバー作成
        self.create_status_bar()
        
        # 中央ウィジェット作成
        self.create_central_widget()
        
        # アクション接続
        self.connect_signals()
    
    def create_menu_bar(self):
        """メニューバーを作成"""
        menubar = self.menuBar()
        
        # ファイルメニュー
        file_menu = menubar.addMenu('ファイル(&F)')
        
        open_action = QAction('開く(&O)', self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction('保存(&S)', self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('終了(&X)', self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 表示メニュー
        view_menu = menubar.addMenu('表示(&V)')
        
        reset_view_action = QAction('表示リセット', self)
        reset_view_action.triggered.connect(self.reset_view)
        view_menu.addAction(reset_view_action)
        
        # ツールメニュー
        tools_menu = menubar.addMenu('ツール(&T)')
        
        settings_action = QAction('設定(&S)', self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
        # ヘルプメニュー
        help_menu = menubar.addMenu('ヘルプ(&H)')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """ツールバーを作成"""
        toolbar = self.addToolBar('メイン')
        toolbar.setMovable(False)
        
        # ファイル操作
        open_action = QAction('開く', self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        save_action = QAction('保存', self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # 表示制御
        reset_action = QAction('リセット', self)
        reset_action.triggered.connect(self.reset_view)
        toolbar.addAction(reset_action)
    
    def create_status_bar(self):
        """ステータスバーを作成"""
        self.status_bar = self.statusBar()
        
        # 情報表示ラベル
        self.status_label = QLabel("準備完了")
        self.status_bar.addWidget(self.status_label)
        
        # データ情報表示
        self.data_info_label = QLabel("データなし")
        self.status_bar.addPermanentWidget(self.data_info_label)
    
    def create_central_widget(self):
        """中央ウィジェットを作成"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # メインレイアウト
        main_layout = QHBoxLayout(central_widget)
        
        # スプリッター作成
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左側：パラメータ制御パネル
        try:
            self.controls = ParameterControls()
            splitter.addWidget(self.controls)
        except NameError:
            # ParameterControlsが未実装の場合の代替
            controls_placeholder = QLabel("パラメータ制御パネル\n（実装予定）")
            controls_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            controls_placeholder.setMinimumWidth(300)
            splitter.addWidget(controls_placeholder)
            self.controls = controls_placeholder
        
        # 右側：スペクトル表示エリア
        try:
            self.spectrum_viewer = SpectrumViewer()
            splitter.addWidget(self.spectrum_viewer)
        except NameError:
            # SpectrumViewerが未実装の場合の代替
            viewer_placeholder = QLabel("スペクトル表示エリア\n（実装予定）")
            viewer_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            splitter.addWidget(viewer_placeholder)
            self.spectrum_viewer = viewer_placeholder
        
        # スプリッターの比率設定
        splitter.setSizes([300, 900])
    
    def connect_signals(self):
        """シグナルとスロットを接続"""
        # データロード時の処理
        self.data_loaded.connect(self.on_data_loaded)
        
        # 設定変更時の処理
        self.settings_changed.connect(self.on_settings_changed)
    
    def open_file(self):
        """ファイルを開く"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "2dir NMRデータファイルを開く",
            "",
            "全サポート形式 (*.nmr *.fid *.dat *.txt *.csv *.h5);;NMR Files (*.nmr *.fid);;Text Files (*.txt *.dat);;CSV Files (*.csv);;HDF5 Files (*.h5)"
        )
        
        if file_path:
            try:
                self.status_label.setText("データ読み込み中...")
                data = self.data_loader.load_data(file_path)
                self.current_data = data
                self.data_loaded.emit(data)
                self.status_label.setText(f"読み込み完了: {Path(file_path).name}")
            except Exception as e:
                QMessageBox.critical(self, "エラー", f"ファイルの読み込みに失敗しました:\n{str(e)}")
                self.status_label.setText("読み込み失敗")
    
    def save_file(self):
        """ファイルを保存"""
        if self.current_data is None:
            QMessageBox.warning(self, "警告", "保存するデータがありません")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "データを保存",
            "",
            "HDF5 Files (*.h5);;CSV Files (*.csv);;Text Files (*.txt)"
        )
        
        if file_path:
            try:
                # ファイル拡張子から形式を判定
                format_map = {'.h5': 'h5', '.csv': 'csv', '.txt': 'txt'}
                file_format = format_map.get(Path(file_path).suffix, 'h5')
                
                self.data_loader.save_data(self.current_data, file_path, file_format)
                self.status_label.setText(f"保存完了: {Path(file_path).name}")
            except Exception as e:
                QMessageBox.critical(self, "エラー", f"ファイルの保存に失敗しました:\n{str(e)}")
    
    def reset_view(self):
        """表示をリセット"""
        if hasattr(self.spectrum_viewer, 'reset_view'):
            self.spectrum_viewer.reset_view()
        self.status_label.setText("表示をリセットしました")
    
    def show_settings(self):
        """設定ダイアログを表示"""
        try:
            dialog = SettingsDialog(self.settings, self)
            if dialog.exec() == dialog.DialogCode.Accepted:
                self.settings = dialog.get_settings()
                self.settings_changed.emit(self.settings)
        except NameError:
            QMessageBox.information(self, "情報", "設定ダイアログは実装予定です")
    
    def show_about(self):
        """Aboutダイアログを表示"""
        try:
            dialog = AboutDialog(self)
            dialog.exec()
        except NameError:
            QMessageBox.about(
                self,
                "About 2dir-insight",
                "2dir-insight v0.1.0\n\n"
                "2次元NMRスペクトロスコピー学習システム\n"
                "教育および研究目的で開発されました。"
            )
    
    def on_data_loaded(self, data):
        """データロード時の処理"""
        # データ情報更新
        info = self.data_loader.get_data_info(data)
        shape_str = f"{info['shape'][0]}×{info['shape'][1]}"
        self.data_info_label.setText(f"データサイズ: {shape_str}")
        
        # スペクトル表示更新
        if hasattr(self.spectrum_viewer, 'set_data'):
            self.spectrum_viewer.set_data(data)
        
        # パラメータ制御更新
        if hasattr(self.controls, 'set_data'):
            self.controls.set_data(data)
    
    def on_settings_changed(self, settings):
        """設定変更時の処理"""
        # 各コンポーネントに設定を適用
        if hasattr(self.spectrum_viewer, 'apply_settings'):
            self.spectrum_viewer.apply_settings(settings)
        
        if hasattr(self.controls, 'apply_settings'):
            self.controls.apply_settings(settings)
    
    def update_status(self):
        """ステータス更新（定期実行）"""
        # メモリ使用量やその他の情報を表示する場合
        pass
    
    def load_settings(self):
        """設定を読み込み"""
        # 設定ファイルから読み込み（実装予定）
        self.settings = {
            'theme': 'light',
            'language': 'ja',
            'auto_save': True
        }
    
    def save_settings(self):
        """設定を保存"""
        # 設定ファイルに保存（実装予定）
        pass
    
    def closeEvent(self, event):
        """アプリケーション終了時の処理"""
        self.save_settings()
        event.accept() 