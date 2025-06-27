#!/usr/bin/env python3
"""
GUI環境確認スクリプト - check_gui_environment.py

このスクリプトはPyQt6 GUI環境が正常に動作するかを確認し、
問題がある場合の解決方法を提案します。
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


def check_display_variable():
    """DISPLAY環境変数をチェック"""
    display = os.environ.get('DISPLAY')
    print(f"DISPLAY環境変数: {display}")
    
    if not display:
        print("❌ DISPLAY環境変数が設定されていません")
        return False
    
    print("✅ DISPLAY環境変数が設定されています")
    return True


def check_x11_socket():
    """X11ソケットの存在確認"""
    x11_socket = Path("/tmp/.X11-unix")
    
    if x11_socket.exists():
        print("✅ X11ソケットが利用可能です")
        socket_files = list(x11_socket.glob("X*"))
        print(f"   利用可能なソケット: {len(socket_files)} 個")
        return True
    else:
        print("❌ X11ソケットが見つかりません")
        return False


def check_qt_libraries():
    """Qt関連ライブラリの確認"""
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QT_VERSION_STR
        from PyQt6 import QtCore
        
        print(f"✅ PyQt6が正常にインストールされています")
        print(f"   PyQt6バージョン: {QtCore.PYQT_VERSION_STR}")
        print(f"   Qtバージョン: {QT_VERSION_STR}")
        return True
        
    except ImportError as e:
        print(f"❌ PyQt6のインポートに失敗: {e}")
        return False


def check_system_packages():
    """システムパッケージの確認"""
    required_packages = [
        'libgl1-mesa-glx',
        'libxcb-xinerama0', 
        'fonts-dejavu-core'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            result = subprocess.run(
                ['dpkg', '-l', package], 
                capture_output=True, 
                text=True,
                check=False
            )
            if result.returncode != 0:
                missing_packages.append(package)
        except FileNotFoundError:
            print("❌ dpkgコマンドが見つかりません（非Debian系システム）")
            return True  # 他のシステムでは無視
    
    if missing_packages:
        print(f"❌ 不足しているパッケージ: {missing_packages}")
        return False
    else:
        print("✅ 必要なシステムパッケージが揃っています")
        return True


def run_simple_gui_test():
    """簡単なGUIテストを実行"""
    try:
        from PyQt6.QtWidgets import QApplication, QWidget, QLabel
        from PyQt6.QtCore import Qt, QTimer
        
        print("GUI基本テストを実行中...")
        
        app = QApplication([])
        
        # テストウィンドウ作成
        window = QWidget()
        window.setWindowTitle('2dir-insight GUI Test')
        window.setGeometry(100, 100, 300, 100)
        
        label = QLabel('GUI環境テスト成功！', window)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setGeometry(50, 30, 200, 40)
        
        window.show()
        
        # 3秒後に自動終了
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(3000)
        
        print("✅ GUI基本テスト成功（3秒間表示）")
        result = app.exec()
        
        return result == 0
        
    except Exception as e:
        print(f"❌ GUI基本テスト失敗: {e}")
        return False


def show_troubleshooting_guide():
    """トラブルシューティングガイドを表示"""
    print("\n" + "="*60)
    print("🔧 GUI環境のトラブルシューティング")
    print("="*60)
    
    system = platform.system()
    
    if system == "Linux":
        print("""
Linux環境での解決方法:

1. X11フォワーディングを有効化:
   export DISPLAY=:0
   
2. X11サーバーへのアクセス許可:
   xhost +local:docker
   
3. VSCode Dev Containerの再起動:
   Command Palette > "Dev Containers: Rebuild Container"
        """)
        
    elif system == "Darwin":  # macOS
        print("""
macOS環境での解決方法:

1. XQuartzをインストール:
   brew install --cask xquartz
   
2. XQuartzを起動してX11フォワーディングを有効化
   
3. DISPLAY環境変数を設定:
   export DISPLAY=host.docker.internal:0
        """)
        
    else:  # Windows
        print("""
Windows環境での解決方法:

1. VcXsrv または Xming をインストール:
   - VcXsrv: https://sourceforge.net/projects/vcxsrv/
   - Xming: https://sourceforge.net/projects/xming/
   
2. X11サーバーを起動（アクセス制御を無効化）

3. DISPLAY環境変数を設定:
   export DISPLAY=host.docker.internal:0.0
   
4. WSL2使用時の追加設定が必要な場合があります
        """)


def main():
    """メイン関数"""
    print("🔍 2dir-insight GUI環境診断")
    print("="*60)
    
    print(f"システム情報: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print()
    
    # 各項目をチェック
    results = []
    
    print("1. DISPLAY環境変数チェック")
    results.append(check_display_variable())
    print()
    
    print("2. X11ソケットチェック")
    results.append(check_x11_socket())
    print()
    
    print("3. PyQt6ライブラリチェック")
    qt_ok = check_qt_libraries()
    results.append(qt_ok)
    print()
    
    print("4. システムパッケージチェック")
    results.append(check_system_packages())
    print()
    
    # GUIテスト（Qtが利用可能な場合のみ）
    if qt_ok:
        print("5. GUI基本テスト")
        gui_test_ok = run_simple_gui_test()
        results.append(gui_test_ok)
        print()
    
    # 結果サマリー
    print("="*60)
    print("📊 診断結果サマリー")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 すべてのテストが成功しました！")
        print("2dir-insightのGUIを起動できます:")
        print("python scripts/run_gui.py")
    else:
        print(f"⚠️  {total - passed}/{total} 項目で問題が検出されました")
        show_troubleshooting_guide()
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 