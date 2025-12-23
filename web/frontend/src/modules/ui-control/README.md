# UI & Control Subsystem

## 概述

UI & Control 子系統提供無障礙設計與個人化設定的使用者介面控制模組，專注於提供簡潔直覺的介面，支援掃描、播放與互動，並強調無障礙設計與個人化設定。

## 目標

- 設計簡潔直覺介面，支援掃描、播放、互動
- 跨平台部署（手機、平板、電腦、IoT）
- 無障礙設計與個人化設定

## 技術標準

本模組符合以下無障礙標準：

- **WAI-ARIA 1.2**: Web Accessibility Initiative - Accessible Rich Internet Applications
- **WCAG 2.1 AA**: Web Content Accessibility Guidelines Level AA
- **包容性設計原則**: 生成式 AI 與包容性設計

## 核心元件

### 1. AccessibilitySettings

無障礙設定元件，提供完整的個人化選項。

**功能：**
- 字型大小調整（小、中、大、特大）
- 對比度模式（正常、高對比、反相）
- 減少動畫效果
- 螢幕閱讀器優化
- 鍵盤導航增強

**使用方式：**
```jsx
import { AccessibilitySettings } from './modules/ui-control';

function App() {
  const handleSettingsChange = (settings) => {
    console.log('New settings:', settings);
  };

  return <AccessibilitySettings onSettingsChange={handleSettingsChange} />;
}
```

**ARIA 屬性：**
- `role="dialog"` - 設定面板為對話框
- `aria-labelledby` - 標題關聯
- `aria-modal="true"` - 模態對話框
- `aria-expanded` - 展開狀態
- `aria-describedby` - 描述關聯

### 2. MediaControls

媒體控制元件，提供掃描、播放與互動控制。

**功能：**
- 掃描控制（開始/停止）
- 播放/暫停控制
- 停止功能
- 播放速度調整（0.5x - 2.0x）
- 鍵盤快捷鍵說明

**使用方式：**
```jsx
import { MediaControls } from './modules/ui-control';

function App() {
  return (
    <MediaControls
      onScan={handleScan}
      onPlay={handlePlay}
      onPause={handlePause}
      onStop={handleStop}
      isPlaying={isPlaying}
      isScanning={isScanning}
      disabled={loading}
    />
  );
}
```

**鍵盤快捷鍵：**
- `Space` - 播放/暫停
- `S` - 掃描
- `Esc` - 停止
- `←/→` - 調整速度

### 3. useKeyboardNavigation Hook

自訂 Hook，提供全局鍵盤導航支援。

**使用方式：**
```jsx
import { useKeyboardNavigation } from './modules/ui-control';

function App() {
  useKeyboardNavigation({
    onPlay: handlePlay,
    onPause: handlePause,
    onStop: handleStop,
    onScan: handleScan,
    onSpeedUp: handleSpeedUp,
    onSpeedDown: handleSpeedDown,
  }, true); // 第二個參數為啟用狀態
}
```

### 4. Accessibility Helper 工具

提供輔助函數以管理無障礙功能。

**函數：**
- `applyAccessibilitySettings(settings)` - 應用無障礙設定
- `announceToScreenReader(message, priority)` - 螢幕閱讀器通知
- `setFocusIndicator(enhanced)` - 設定焦點指示器
- `detectSystemPreferences()` - 偵測系統偏好
- `skipToMainContent()` - 跳至主要內容

**使用方式：**
```jsx
import { applyAccessibilitySettings, announceToScreenReader } from './modules/ui-control';

// 應用設定
applyAccessibilitySettings({
  fontSize: 'large',
  contrast: 'high',
  reducedMotion: true
});

// 通知螢幕閱讀器
announceToScreenReader('頁面已載入', 'polite');
```

## 跨平台支援

本模組設計支援多種平台：

### 手機與平板
- 響應式設計，適應不同螢幕尺寸
- 觸控友善的控制元素
- 手勢支援（未來擴展）

### 桌面電腦
- 完整的鍵盤導航
- 滑鼠懸停效果
- 拖放支援（未來擴展）

### IoT 裝置
- 簡化的控制介面
- 語音控制整合（未來擴展）
- 低功耗模式（未來擴展）

## 無障礙功能詳解

### 視覺無障礙
- **字型大小調整**：支援 4 種字型大小
- **高對比模式**：提供高對比與反相配色
- **焦點指示器**：清晰的鍵盤焦點提示

### 聽覺無障礙
- **視覺替代**：所有音訊內容提供視覺回饋
- **音量控制**：可調整音量與播放速度

### 運動無障礙
- **減少動畫**：支援 `prefers-reduced-motion`
- **鍵盤操作**：所有功能皆可透過鍵盤操作
- **語音控制**：（規劃中）

### 認知無障礙
- **簡潔介面**：直覺的控制元素
- **一致性**：統一的設計語言
- **明確回饋**：即時的操作回饋

## 測試

模組包含完整的單元測試：

```bash
npm test
```

測試涵蓋：
- 元件渲染
- 使用者互動
- ARIA 屬性驗證
- 無障礙功能測試

## 文獻引用

1. **無障礙介面設計綜述**
   - 提供無障礙設計的最佳實踐指南

2. **WAI-ARIA 1.2 標準**
   - W3C 制定的無障礙富互聯網應用標準

3. **生成式 AI 與包容性設計**
   - 探討如何運用 AI 提升無障礙體驗

4. **跨平台 UI 框架**
   - Flutter、React Native 等框架的比較與應用

## 未來發展

- [ ] 語音控制整合
- [ ] 手勢導航支援
- [ ] 更多語言支援
- [ ] 深色/淺色主題切換
- [ ] 自訂主題配色
- [ ] 離線模式支援
- [ ] 雲端設定同步

## 授權

本模組遵循專案主要授權協議。
