#!/bin/bash
# macOS環境でのGUI設定スクリプト

echo "🍎 macOS環境でのGUI設定を開始..."

# XQuartzの確認
if ! command -v xquartz &> /dev/null; then
    echo "❌ XQuartzがインストールされていません"
    echo "📦 以下のコマンドでインストールしてください:"
    echo "   brew install --cask xquartz"
    echo "   または https://www.xquartz.org/ からダウンロード"
    exit 1
fi

echo "✅ XQuartzが利用可能です"

# XQuartzプロセスの確認
if ! pgrep -x "Xquartz" > /dev/null; then
    echo "🚀 XQuartzを起動中..."
    open -a XQuartz
    sleep 3
fi

# DISPLAY環境変数の設定
export DISPLAY=host.docker.internal:0
echo "export DISPLAY=host.docker.internal:0" >> ~/.bashrc

# X11フォワーディングの許可
echo "🔓 X11アクセス許可を設定中..."
xhost +host.docker.internal

echo "✅ macOS GUI環境の設定が完了しました"
echo ""
echo "📋 次のステップ:"
echo "1. Dev Containerを再起動してください"
echo "2. GUI環境の確認: python scripts/check_gui_environment.py"
echo "3. 2dir-insight GUI起動: python scripts/run_gui.py"
echo ""
echo "💡 トラブルシューティング:"
echo "   - XQuartzの設定で「ネットワーククライアントからの接続を許可」を有効化"
echo "   - セキュリティ設定でXQuartzの権限を確認" 