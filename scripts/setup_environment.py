#!/usr/bin/env python3
"""
2dir-insight 環境セットアップスクリプト

このスクリプトは開発環境や実行環境の初期化を行います。
"""

import os
import sys
import subprocess
from pathlib import Path
import json


def check_python_version():
    """Python バージョンをチェック"""
    if sys.version_info < (3, 12):
        print("エラー: Python 3.12 以上が必要です")
        print(f"現在のバージョン: {sys.version}")
        return False
    print(f"Python バージョン: {sys.version} ✓")
    return True


def create_directories():
    """必要なディレクトリを作成"""
    project_root = Path(__file__).parent.parent
    directories = [
        "data/sample_spectra/cosy",
        "data/sample_spectra/tocsy", 
        "data/sample_spectra/noesy",
        "data/tutorials",
        "notebooks/tutorials",
        "notebooks/examples",
        "notebooks/playground",
        "tests/test_core",
        "tests/test_gui",
        "tests/test_visualization",
        "docs/tutorial",
        "docs/api"
    ]
    
    for dir_path in directories:
        full_path = project_root / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"ディレクトリ作成: {dir_path} ✓")


def install_dependencies():
    """依存関係をインストール"""
    project_root = Path(__file__).parent.parent
    requirements_file = project_root / "requirements.txt"
    
    if not requirements_file.exists():
        print("エラー: requirements.txt が見つかりません")
        return False
    
    try:
        print("依存関係をインストール中...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("依存関係のインストール完了 ✓")
        return True
    except subprocess.CalledProcessError as e:
        print(f"エラー: 依存関係のインストールに失敗しました: {e}")
        return False


def install_package():
    """パッケージを開発モードでインストール"""
    project_root = Path(__file__).parent.parent
    
    try:
        print("パッケージを開発モードでインストール中...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-e", str(project_root)
        ])
        print("パッケージのインストール完了 ✓")
        return True
    except subprocess.CalledProcessError as e:
        print(f"エラー: パッケージのインストールに失敗しました: {e}")
        return False


def create_sample_config():
    """サンプル設定ファイルを作成"""
    project_root = Path(__file__).parent.parent
    config_dir = project_root / "config"
    
    # ユーザー設定ファイルの例を作成
    user_config = {
        "user_preferences": {
            "default_workspace": str(project_root / "data"),
            "recent_files": [],
            "theme": "light",
            "language": "ja"
        }
    }
    
    user_config_file = config_dir / "user_settings.json"
    with open(user_config_file, "w", encoding="utf-8") as f:
        json.dump(user_config, f, indent=2, ensure_ascii=False)
    
    print(f"ユーザー設定ファイル作成: {user_config_file} ✓")


def main():
    """メイン関数"""
    print("=== 2dir-insight 環境セットアップ ===\n")
    
    # Python バージョンチェック
    if not check_python_version():
        sys.exit(1)
    
    # ディレクトリ作成
    print("\nディレクトリ構造を作成中...")
    create_directories()
    
    # 依存関係インストール
    print("\n依存関係をインストール中...")
    if not install_dependencies():
        sys.exit(1)
    
    # パッケージインストール
    print("\nパッケージをインストール中...")
    if not install_package():
        sys.exit(1)
    
    # 設定ファイル作成
    print("\n設定ファイルを作成中...")
    create_sample_config()
    
    print("\n=== セットアップ完了 ===")
    print("以下のコマンドでGUIを起動できます:")
    print("python scripts/run_gui.py")


if __name__ == "__main__":
    main() 