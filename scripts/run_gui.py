#!/usr/bin/env python3
"""
2dir-insight GUI起動スクリプト

このスクリプトは2次元NMRスペクトロスコピー学習システムの
メインGUIアプリケーションを起動します。
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    from gui.main_window import MainWindow
except ImportError as e:
    print(f"エラー: 必要なライブラリがインストールされていません: {e}")
    print("pip install -r requirements.txt を実行してください")
    sys.exit(1)


def setup_application():
    """アプリケーション設定を初期化"""
    app = QApplication(sys.argv)
    app.setApplicationName("2dir-insight")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("2dir-insight Team")
    
    # 高DPI対応
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    return app


def main():
    """メイン関数"""
    print("2dir-insight を起動中...")
    
    app = setup_application()
    
    try:
        # メインウィンドウを作成・表示
        main_window = MainWindow()
        main_window.show()
        
        print("GUI が正常に起動しました")
        
        # アプリケーション実行
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"エラー: アプリケーションの起動に失敗しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 