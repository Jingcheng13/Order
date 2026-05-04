# 高级参考：组件模式与代码模板

本文件包含在实现特定任务时可参考的高级模式与代码模板。

## 目录

1. [响应式幻灯片引擎](#响应式幻灯片引擎)
2. [设备模拟外框](#设备模拟外框)
3. [Tweaks 面板实现](#tweaks-面板实现)
4. [动画时间轴引擎](#动画时间轴引擎)
5. [设计画布（多方案对比）](#设计画布)
6. [深色模式切换](#深色模式切换)
7. [数据可视化模板](#数据可视化模板)

---

## 响应式幻灯片引擎

用于构建可自适应任意视口的固定尺寸演示文稿。

**关键约定**：
- 内部数组使用 0 起始索引，**但向用户显示的数字始终为 1 起始**
- 每张 `<section class="slide">` 添加 `data-screen-label="01 标题"`、`data-screen-label="02 议程"` 等属性，以便引用
- 控制按钮置于 `.stage` 缩放容器**外部**，确保在小屏幕上仍可点击

```html
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { 
    background: #000; 
    display: flex; 
    align-items: center; 
    justify-content: center;
    height: 100vh;
    overflow: hidden;
    font-family: system-ui, sans-serif;
  }
  .stage {
    width: 1920px;
    height: 1080px;
    position: relative;
    transform-origin: center center;
  }
  .slide {
    position: absolute;
    inset: 0;
    display: none;
    padding: 80px;
  }
  .slide.active { display: flex; }
  .controls {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 12px;
    z-index: 1000;
  }
  .controls button {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    background: rgba(255,255,255,0.15);
    color: white;
    cursor: pointer;
    font-size: 14px;
  }
  .slide-counter {
    position: fixed;
    bottom: 20px;
    right: 20px;
    color: rgba(255,255,255,0.6);
    font-size: 14px;
  }
</style>

<script>
  // 自适应缩放
  function scaleStage() {
    const stage = document.querySelector('.stage');
    const scaleX = window.innerWidth / 1920;
    const scaleY = window.innerHeight / 1080;
    const scale = Math.min(scaleX, scaleY);
    stage.style.transform = `scale(${scale})`;
  }
  window.addEventListener('resize', scaleStage);
  scaleStage();

  // 幻灯片导航
  let current = parseInt(localStorage.getItem('slideIndex') || '0');
  const slides = document.querySelectorAll('.slide');
  
  function showSlide(n) {
    current = Math.max(0, Math.min(n, slides.length - 1));
    slides.forEach((s, i) => s.classList.toggle('active', i === current));
    localStorage.setItem('slideIndex', current);
    // 向用户显示 1 起始索引，内部存储 0 起始索引
    document.querySelector('.slide-counter').textContent = `${current + 1} / ${slides.length}`;
  }
  
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight' || e.key === ' ') showSlide(current + 1);
    if (e.key === 'ArrowLeft') showSlide(current - 1);
  });
  
  showSlide(current);
</script>
```

---

## 设备模拟外框

### iPhone 外框

```jsx
const IPhoneFrame = ({ children, title = "应用" }) => (
  <div style={{
    width: 390,
    height: 844,
    borderRadius: 48,
    border: '12px solid #1a1a1a',
    overflow: 'hidden',
    position: 'relative',
    boxShadow: '0 25px 50px -12px rgba(0,0,0,0.25)',
    background: '#fff'
  }}>
    {/* 状态栏 */}
    <div style={{
      height: 54,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 24px',
      fontSize: 14,
      fontWeight: 600
    }}>
      <span>9:41</span>
      <div style={{
        width: 126,
        height: 34,
        background: '#1a1a1a',
        borderRadius: 20,
        position: 'absolute',
        left: '50%',
        transform: 'translateX(-50%)',
        top: 8
      }} />
      <span>⚡ 📶</span>
    </div>
    {/* 内容区域 */}
    <div style={{ height: 'calc(100% - 54px)', overflow: 'auto' }}>
      {children}
    </div>
    {/* 底部指示条 */}
    <div style={{
      position: 'absolute',
      bottom: 8,
      left: '50%',
      transform: 'translateX(-50%)',
      width: 134,
      height: 5,
      background: '#1a1a1a',
      borderRadius: 3
    }} />
  </div>
);
```

### 浏览器窗口外框

```jsx
const BrowserFrame = ({ children, url = "https://example.com", title = "页面" }) => (
  <div style={{
    borderRadius: 12,
    overflow: 'hidden',
    boxShadow: '0 25px 50px -12px rgba(0,0,0,0.25)',
    border: '1px solid #e5e5e5'
  }}>
    {/* 标题栏 */}
    <div style={{
      background: '#f5f5f5',
      padding: '12px 16px',
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      borderBottom: '1px solid #e5e5e5'
    }}>
      <div style={{ display: 'flex', gap: 8 }}>
        <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#ff5f57' }} />
        <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#febc2e' }} />
        <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#28c840' }} />
      </div>
      <div style={{
        flex: 1,
        background: '#fff',
        borderRadius: 6,
        padding: '6px 12px',
        fontSize: 13,
        color: '#666',
        border: '1px solid #e0e0e0'
      }}>
        {url}
      </div>
    </div>
    {/* 内容区域 */}
    <div style={{ background: '#fff' }}>
      {children}
    </div>
  </div>
);
```

---

## Tweaks 面板实现

```jsx
const TweaksPanel = ({ config, onChange, visible }) => {
  if (!visible) return null;
  
  return (
    <div style={{
      position: 'fixed',
      bottom: 20,
      right: 20,
      width: 280,
      background: 'rgba(24, 24, 27, 0.95)',
      backdropFilter: 'blur(12px)',
      borderRadius: 12,
      padding: 16,
      color: '#fff',
      fontSize: 13,
      zIndex: 9999,
      boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
      border: '1px solid rgba(255,255,255,0.1)'
    }}>
      <div style={{ fontWeight: 600, marginBottom: 12, fontSize: 14 }}>Tweaks</div>
      
      {Object.entries(config).map(([key, value]) => (
        <div key={key} style={{ marginBottom: 12 }}>
          <label style={{ display: 'block', marginBottom: 4, opacity: 0.7 }}>
            {key}
          </label>
          {typeof value === 'boolean' ? (
            <input
              type="checkbox"
              checked={value}
              onChange={e => onChange({ ...config, [key]: e.target.checked })}
            />
          ) : typeof value === 'number' ? (
            <input
              type="range"
              min="0"
              max="100"
              value={value}
              onChange={e => onChange({ ...config, [key]: Number(e.target.value) })}
              style={{ width: '100%' }}
            />
          ) : value.startsWith('#') ? (
            <input
              type="color"
              value={value}
              onChange={e => onChange({ ...config, [key]: e.target.value })}
            />
          ) : (
            <input
              type="text"
              value={value}
              onChange={e => onChange({ ...config, [key]: e.target.value })}
              style={{
                width: '100%',
                background: 'rgba(255,255,255,0.1)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: 4,
                padding: '4px 8px',
                color: '#fff'
              }}
            />
          )}
        </div>
      ))}
    </div>
  );
};
```

---

## 动画时间轴引擎

```jsx
const useTime = (duration = 5000) => {
  const [time, setTime] = React.useState(0);
  const [playing, setPlaying] = React.useState(true);
  const frameRef = React.useRef();
  const startRef = React.useRef();
  
  React.useEffect(() => {
    if (!playing) return;
    const animate = (timestamp) => {
      if (!startRef.current) startRef.current = timestamp;
      const elapsed = (timestamp - startRef.current) % duration;
      setTime(elapsed / duration); // 0 到 1
      frameRef.current = requestAnimationFrame(animate);
    };
    frameRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frameRef.current);
  }, [playing, duration]);
  
  return { time, playing, setPlaying };
};

const Easing = {
  linear: t => t,
  easeInOut: t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t,
  easeOut: t => 1 - Math.pow(1 - t, 3),
  easeIn: t => t * t * t,
  spring: t => 1 - Math.pow(Math.E, -6 * t) * Math.cos(8 * t)
};

const interpolate = (t, from, to, easing = Easing.easeInOut) => {
  const progress = easing(Math.max(0, Math.min(1, t)));
  return from + (to - from) * progress;
};

// 使用示例：
// const { time } = useTime(3000);
// const opacity = interpolate(time, 0, 1);
// const x = interpolate(time, -100, 0, Easing.spring);
```

---

## 设计画布

用于并排展示多个设计方案以进行对比：

```jsx
const DesignCanvas = ({ options, columns = 3 }) => (
  <div style={{
    display: 'grid',
    gridTemplateColumns: `repeat(${columns}, 1fr)`,
    gap: 24,
    padding: 40,
    background: '#f8f9fa',
    minHeight: '100vh'
  }}>
    {options.map((option, i) => (
      <div key={i} style={{
        background: '#fff',
        borderRadius: 12,
        overflow: 'hidden',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
      }}>
        <div style={{
          padding: '12px 16px',
          borderBottom: '1px solid #eee',
          fontSize: 13,
          fontWeight: 600,
          color: '#666'
        }}>
          方案 {String.fromCharCode(65 + i)}: {option.label}
        </div>
        <div style={{ padding: 16 }}>
          {option.content}
        </div>
      </div>
    ))}
  </div>
);
```

---

## 深色模式切换

```jsx
const ThemeProvider = ({ children }) => {
  const [dark, setDark] = React.useState(
    window.matchMedia('(prefers-color-scheme: dark)').matches
  );
  
  const theme = dark ? {
    bg: '#0a0a0b',
    surface: '#18181b',
    border: '#27272a',
    text: '#fafafa',
    textMuted: '#a1a1aa',
    primary: '#3b82f6'
  } : {
    bg: '#ffffff',
    surface: '#f4f4f5',
    border: '#e4e4e7',
    text: '#18181b',
    textMuted: '#71717a',
    primary: '#2563eb'
  };
  
  return (
    <ThemeContext.Provider value={{ theme, dark, setDark }}>
      <div style={{ background: theme.bg, color: theme.text, minHeight: '100vh' }}>
        {children}
      </div>
    </ThemeContext.Provider>
  );
};
```

---

## 数据可视化模板

### Chart.js 快速上手

```html
<canvas id="myChart" width="800" height="400"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
  const ctx = document.getElementById('myChart').getContext('2d');
  new Chart(ctx, {
    type: 'line', // 可选 bar, pie, doughnut, radar 等
    data: {
      labels: ['一月', '二月', '三月', '四月', '五月', '六月'],
      datasets: [{
        label: '收入',
        data: [12, 19, 3, 5, 2, 3],
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { beginAtZero: true, grid: { color: '#f0f0f0' } },
        x: { grid: { display: false } }
      }
    }
  });
</script>
```

---

## 色彩系统最佳实践

使用 oklch 定义协调的色彩系统：

```css
:root {
  /* 基于 oklch 的色彩系统 */
  --primary-h: 250;  /* 色相 */
  --primary: oklch(0.55 0.25 var(--primary-h));
  --primary-light: oklch(0.75 0.15 var(--primary-h));
  --primary-dark: oklch(0.35 0.2 var(--primary-h));
  
  /* 中性色 */
  --gray-50: oklch(0.98 0.002 250);
  --gray-100: oklch(0.96 0.004 250);
  --gray-200: oklch(0.92 0.006 250);
  --gray-300: oklch(0.87 0.008 250);
  --gray-400: oklch(0.71 0.01 250);
  --gray-500: oklch(0.55 0.014 250);
  --gray-600: oklch(0.45 0.014 250);
  --gray-700: oklch(0.37 0.014 250);
  --gray-800: oklch(0.27 0.014 250);
  --gray-900: oklch(0.21 0.014 250);
}
```

---

## 字体推荐（非默认选择）

> ⚠️ **以下为基于经验的建议，并非硬性规定。**
> - 始终优先使用品牌或设计系统已指定的字体；仅当用户未提供任何字体方案时，才参考此表。
> - 唯一的硬性规则：**避免使用 Inter / Roboto / Arial / Fraunces / system-ui —— 这些字体已被 AI 生成内容过度使用**，会立刻让人感觉“这是 AI 拼凑的”。
> - 选择字体时，关注“个性契合度”而非“当前流行度”。下表仅列出常见的高品质选项，并非详尽无遗。

| 用途 | 推荐 | Google Fonts 名称 |
|------|------|------------------|
| 现代标题 | Plus Jakarta Sans | Plus+Jakarta+Sans |
| 典雅正文 | Outfit | Outfit |
| 技术感 | Space Grotesk | Space+Grotesk |
| 高端品牌 | Sora | Sora |
| 编辑质感 | Newsreader | Newsreader |
| 手写风格 | Caveat | Caveat |
| 等宽/代码 | JetBrains Mono | JetBrains+Mono |

```html
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

---

## 配色 × 字体搭配参考

> ⚠️ **以下为基于经验的搭配建议，并非硬性规定。** 当你**完全没有设计上下文**时，从中选一个作为起点——这远比从 Inter + #3b82f6 开始要好。
> 一旦用户提供了品牌 / 设计系统 / 参考站点，立即放下此表，遵循他们的素材。

用于快速建立具有个性的视觉系统：

| 风格 | 主色 (oklch) | 字体搭配 | 最适合 |
|---|---|---|---|
| 现代科技 | `oklch(0.55 0.25 250)` 蓝紫色 | Space Grotesk + Inter | SaaS、开发工具、AI 产品 |
| 优雅编辑 | `oklch(0.35 0.10 30)` 暖棕色 | Newsreader + Outfit | 内容平台、博客、编辑类产品 |
| 高端品牌 | `oklch(0.20 0.02 250)` 近黑色 | Sora + Plus Jakarta Sans | 奢侈品、咨询、金融 |
| 活泼消费 | `oklch(0.70 0.20 30)` 珊瑚色 | Plus Jakarta Sans + Outfit | 电商、生活方式、社交 |
| 简约专业 | `oklch(0.50 0.15 200)` 蓝绿色 | Outfit + Space Grotesk | 数据产品、仪表盘、B2B |
| 匠心温暖 | `oklch(0.55 0.15 80)` 焦糖色 | Caveat（装饰） + Newsreader | 餐饮、教育、创意 |

避免以下组合：
- ❌ Inter + Roboto + 蓝色按钮（典型的 AI 审美）
- ❌ Fraunces + 紫粉渐变（已被滥用）
- ❌ 超过三种字体家族（视觉混乱）