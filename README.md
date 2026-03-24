# Python Tetris

這是一個使用 Python 與 Pygame 製作的俄羅斯方塊 (Tetris) 遊戲。

## 功能特色 (Features)
- 完整的核心方塊機制：移動、旋轉、加速下落與直接到底 (Hard drop)。
- 碰撞偵測與消除判定。
- 內建音效支援 (包含方塊移動、旋轉、下落、消除與遊戲結束)。

## 環境需求 (Requirements)
- Python 3.x
- `pygame`
- `numpy`

## 安裝與執行方式 (Installation & Usage)

1. **建立並啟動虛擬環境 (建議選項)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows 環境請使用 venv\Scripts\activate
   ```

2. **安裝依賴套件**
   ```bash
   pip install -r requirements.txt
   ```

3. **執行遊戲**
   ```bash
   python tetris.py
   ```

## 遊戲控制 (Controls)
- `←` / `→` (左右方向鍵): 左右移動方塊
- `↑` (上方向鍵): 旋轉方塊
- `↓` (下方向鍵): 加速下落
- `空白鍵 (Space)`: 直接掉到底層 (Hard Drop)

## 授權 (License)
本專案僅供學習與參考使用。
