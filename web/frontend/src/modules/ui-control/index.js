/**
 * UI & Control Subsystem
 * 提供無障礙設計與個人化設定的使用者介面控制模組
 * 
 * 符合標準：
 * - WAI-ARIA 1.2
 * - WCAG 2.1 AA
 * 
 * 功能：
 * - 無障礙設定（字型、對比度、動畫等）
 * - 媒體控制（掃描、播放、互動）
 * - 鍵盤導航支援
 * - 螢幕閱讀器優化
 * - 跨平台支援（手機、平板、電腦、IoT）
 */

export { default as AccessibilitySettings } from './components/AccessibilitySettings';
export { default as MediaControls } from './components/MediaControls';
export { default as useKeyboardNavigation } from './hooks/useKeyboardNavigation';
export * from './utils/accessibilityHelper';
