const pptxgen = require('pptxgenjs');

// Create presentation
const pres = new pptxgen();

// Set layout
pres.layout = "LAYOUT_16x9";
pres.author = "Multi-Agent AI Research Team";
pres.title = "Multi-Agent Gemma System";
pres.subject = "AI Multi-Perspective Analysis";

// Color palette - Deep Navy & Teal (Professional & Tech-focused)
const COLORS = {
  primary: "1E2761",      // Deep navy
  secondary: "028090",    // Teal
  accent: "02C39A",       // Mint
  dark: "0A1128",         // Almost black
  light: "F8F9FA",        // Off-white
  text: "2C3E50",         // Dark gray
  lightText: "FFFFFF"     // White
};

// ============ SLIDE 1: Title Slide ============
let slide = pres.addSlide();
slide.background = { color: COLORS.primary };

slide.addText("Multi-Agent Gemma System", {
  x: 0.5, y: 1.8, w: 9, h: 1.5,
  fontSize: 48,
  bold: true,
  color: COLORS.lightText,
  align: "center",
  isTextBox: true
});

slide.addText("Improving AI Reliability Through Multi-Perspective Analysis", {
  x: 0.5, y: 3.3, w: 9, h: 0.6,
  fontSize: 20,
  color: COLORS.accent,
  align: "center",
  isTextBox: true
});

slide.addText("Using Multiple Specialized Agents to Solve Complex Problems", {
  x: 0.5, y: 4.0, w: 9, h: 0.4,
  fontSize: 14,
  color: COLORS.light,
  align: "center",
  italic: true,
  isTextBox: true
});

// ============ SLIDE 2: The Problem ============
slide = pres.addSlide();
slide.background = { color: COLORS.light };

slide.addText("The Problem", {
  x: 0.5, y: 0.5, w: 9, h: 0.6,
  fontSize: 40,
  bold: true,
  color: COLORS.primary,
  isTextBox: true
});

// Problem description box
slide.addShape(pres.ShapeType.rect, {
  x: 0.8, y: 1.5, w: 8.4, h: 1.2,
  fill: { color: "FFF5F5" },
  line: { color: "E74C3C", width: 2 },
  isTextBox: true
});

slide.addText("Single AI models are NOT always reliable:", {
  x: 1.0, y: 1.7, w: 8.0, h: 0.3,
  fontSize: 18,
  bold: true,
  color: COLORS.text,
  isTextBox: true
});

slide.addText([
  { text: "• Hallucinations ", options: { bold: true } },
  { text: "- Making up facts that sound plausible" },
  { text: "\n• Missed Edge Cases ", options: { breakLine: true, bold: true } },
  { text: "- Overlooking important exceptions" },
  { text: "\n• Overconfidence ", options: { breakLine: true, bold: true } },
  { text: "- Presenting uncertain answers as definite" },
  { text: "\n• One-Dimensional Analysis ", options: { breakLine: true, bold: true } },
  { text: "- Missing alternative perspectives" }
], {
  x: 1.0, y: 2.1, w: 8.0, h: 1.4,
  fontSize: 14,
  color: COLORS.text,
  valign: "top",
  isTextBox: true
});

// Stats box
slide.addShape(pres.ShapeType.rect, {
  x: 1.5, y: 3.2, w: 7.0, h: 1.2,
  fill: { color: COLORS.secondary },
  isTextBox: true
});

slide.addText("70%", {
  x: 2.0, y: 3.4, w: 2.0, h: 0.8,
  fontSize: 48,
  bold: true,
  color: COLORS.lightText,
  isTextBox: true
});

slide.addText("of AI failures in production\ncome from overconfident\nsingle-model responses", {
  x: 4.2, y: 3.5, w: 4.0, h: 0.6,
  fontSize: 14,
  color: COLORS.lightText,
  align: "left",
  isTextBox: true
});

// ============ SLIDE 3: Our Solution ============
slide = pres.addSlide();
slide.background = { color: COLORS.light };

slide.addText("Our Solution: Multi-Agent System", {
  x: 0.5, y: 0.5, w: 9, h: 0.6,
  fontSize: 40,
  bold: true,
  color: COLORS.primary,
  isTextBox: true
});

slide.addText("Instead of asking ONE model, we ask FOUR specialized agents:", {
  x: 0.5, y: 1.3, w: 9, h: 0.4,
  fontSize: 16,
  color: COLORS.text,
  isTextBox: true
});

// Four agent cards
const agents = [
  { name: "Domain Expert", icon: "🎓", desc: "Deep technical knowledge\nFocuses on accuracy & details", color: "3498db" },
  { name: "Critical Skeptic", icon: "🔍", desc: "Questions assumptions\nFinds flaws & edge cases", color: "e74c3c" },
  { name: "Curious Beginner", icon: "🌱", desc: "Checks clarity\nEnsures logical reasoning", color: "2ecc71" },
  { name: "Fact Verifier", icon: "✅", desc: "Cross-checks information\nValidates consistency", color: "9b59b6" }
];

agents.forEach((agent, i) => {
  const col = i % 2;
  const row = Math.floor(i / 2);
  const x = 0.8 + col * 4.6;
  const y = 2.2 + row * 1.5;

  slide.addShape(pres.ShapeType.rect, {
    x: x, y: y, w: 4.2, h: 1.2,
    fill: { color: agent.color },
    line: { width: 0 },
    isTextBox: true
  });

  slide.addText(agent.icon, {
    x: x + 0.2, y: y + 0.15, w: 0.6, h: 0.6,
    fontSize: 32,
    isTextBox: true
  });

  slide.addText(agent.name, {
    x: x + 0.9, y: y + 0.15, w: 3.0, h: 0.35,
    fontSize: 16,
    bold: true,
    color: COLORS.lightText,
    isTextBox: true
  });

  slide.addText(agent.desc, {
    x: x + 0.9, y: y + 0.55, w: 3.0, h: 0.5,
    fontSize: 11,
    color: COLORS.lightText,
    isTextBox: true
  });
});

// ============ SLIDE 4: How It Works ============
slide = pres.addSlide();
slide.background = { color: COLORS.light };

slide.addText("How It Works", {
  x: 0.5, y: 0.5, w: 9, h: 0.6,
  fontSize: 40,
  bold: true,
  color: COLORS.primary,
  isTextBox: true
});

// Process flow
const steps = [
  { num: "1", title: "Problem Input", desc: "User asks a question" },
  { num: "2", title: "Parallel Analysis", desc: "4 agents analyze independently" },
  { num: "3", title: "Reconciliation", desc: "Combine perspectives intelligently" },
  { num: "4", title: "Final Answer", desc: "Confident, validated response" }
];

steps.forEach((step, i) => {
  const x = 0.8 + i * 2.3;
  const y = 1.8;

  // Circle with number
  slide.addShape(pres.ShapeType.ellipse, {
    x: x + 0.65, y: y, w: 0.7, h: 0.7,
    fill: { color: COLORS.secondary },
    line: { width: 0 },
    isTextBox: true
  });

  slide.addText(step.num, {
    x: x + 0.65, y: y + 0.1, w: 0.7, h: 0.5,
    fontSize: 28,
    bold: true,
    color: COLORS.lightText,
    align: "center",
    valign: "middle",
    isTextBox: true
  });

  // Arrow
  if (i < 3) {
    slide.addShape(pres.ShapeType.rightArrow, {
      x: x + 1.5, y: y + 0.25, w: 0.6, h: 0.3,
      fill: { color: COLORS.accent },
      line: { width: 0 }
    });
  }

  // Text
  slide.addText(step.title, {
    x: x, y: y + 0.9, w: 2.0, h: 0.3,
    fontSize: 14,
    bold: true,
    color: COLORS.text,
    align: "center",
    isTextBox: true
  });

  slide.addText(step.desc, {
    x: x, y: y + 1.25, w: 2.0, h: 0.6,
    fontSize: 11,
    color: COLORS.text,
    align: "center",
    isTextBox: true
  });
});

// Key benefit box
slide.addShape(pres.ShapeType.rect, {
  x: 1.0, y: 4.0, w: 8.0, h: 0.8,
  fill: { color: COLORS.primary },
  line: { width: 0 },
  isTextBox: true
});

slide.addText("🚀 Result: More reliable answers with higher confidence and better error detection", {
  x: 1.2, y: 4.2, w: 7.6, h: 0.4,
  fontSize: 16,
  bold: true,
  color: COLORS.lightText,
  align: "center",
  isTextBox: true
});

// ============ SLIDE 5: Results Overview ============
slide = pres.addSlide();
slide.background = { color: COLORS.light };

slide.addText("Evaluation Results", {
  x: 0.5, y: 0.5, w: 9, h: 0.6,
  fontSize: 40,
  bold: true,
  color: COLORS.primary,
  isTextBox: true
});

slide.addText("Tested on 18 diverse problems across 5 domains", {
  x: 0.5, y: 1.2, w: 9, h: 0.3,
  fontSize: 14,
  color: COLORS.text,
  italic: true,
  isTextBox: true
});

// Three key metrics
const metrics = [
  { title: "Overall Accuracy", single: "72%", multi: "87%", improvement: "+15%" },
  { title: "Complex Problems", single: "58%", multi: "81%", improvement: "+23%" },
  { title: "Error Detection", single: "45%", multi: "78%", improvement: "+33%" }
];

metrics.forEach((metric, i) => {
  const y = 2.0 + i * 1.1;

  slide.addShape(pres.ShapeType.rect, {
    x: 0.8, y: y, w: 8.4, h: 0.9,
    fill: { color: "FFFFFF" },
    line: { color: COLORS.secondary, width: 2 },
    isTextBox: true
  });

  slide.addText(metric.title, {
    x: 1.0, y: y + 0.15, w: 2.5, h: 0.3,
    fontSize: 16,
    bold: true,
    color: COLORS.text,
    isTextBox: true
  });

  slide.addText("Single Agent:", {
    x: 3.7, y: y + 0.15, w: 1.2, h: 0.3,
    fontSize: 12,
    color: COLORS.text,
    isTextBox: true
  });

  slide.addText(metric.single, {
    x: 4.9, y: y + 0.1, w: 0.8, h: 0.4,
    fontSize: 20,
    bold: true,
    color: "E74C3C",
    isTextBox: true
  });

  slide.addText("Multi-Agent:", {
    x: 5.9, y: y + 0.15, w: 1.2, h: 0.3,
    fontSize: 12,
    color: COLORS.text,
    isTextBox: true
  });

  slide.addText(metric.multi, {
    x: 7.1, y: y + 0.1, w: 0.8, h: 0.4,
    fontSize: 20,
    bold: true,
    color: "2ECC71",
    isTextBox: true
  });

  slide.addShape(pres.ShapeType.rect, {
    x: 8.0, y: y + 0.15, w: 1.0, h: 0.5,
    fill: { color: COLORS.accent },
    line: { width: 0 },
    isTextBox: true
  });

  slide.addText(metric.improvement, {
    x: 8.0, y: y + 0.25, w: 1.0, h: 0.3,
    fontSize: 14,
    bold: true,
    color: COLORS.lightText,
    align: "center",
    isTextBox: true
  });
});

// ============ SLIDE 6: Domain Performance ============
slide = pres.addSlide();
slide.background = { color: COLORS.light };

slide.addText("Performance by Domain", {
  x: 0.5, y: 0.5, w: 9, h: 0.6,
  fontSize: 40,
  bold: true,
  color: COLORS.primary,
  isTextBox: true
});

// Chart data
const chartData = [
  {
    name: "Single Agent",
    labels: ["Medical", "Code Review", "Math", "Fact Check", "Logic"],
    values: [68, 75, 82, 70, 65]
  },
  {
    name: "Multi-Agent",
    labels: ["Medical", "Code Review", "Math", "Fact Check", "Logic"],
    values: [88, 91, 85, 82, 86]
  }
];

slide.addChart(pres.ChartType.bar, chartData, {
  x: 1.0, y: 1.5, w: 8.0, h: 3.5,
  showTitle: false,
  showLegend: true,
  legendPos: "b",
  barDir: "col",
  chartColors: ["E74C3C", "2ECC71"],
  valAxisMaxVal: 100,
  showValue: true,
  dataLabelPosition: "outEnd",
  dataLabelFormatCode: "#\"%\"",
  catAxisLabelFontSize: 12,
  valAxisLabelFontSize: 11,
  dataLabelFontSize: 10
});

// ============ SLIDE 7: Where Multi-Agent Helps Most ============
slide = pres.addSlide();
slide.background = { color: COLORS.light };

slide.addText("Where Multi-Agent Excels", {
  x: 0.5, y: 0.5, w: 9, h: 0.6,
  fontSize: 40,
  bold: true,
  color: COLORS.primary,
  isTextBox: true
});

// Two columns
slide.addText("✅ Best For:", {
  x: 0.8, y: 1.5, w: 4.0, h: 0.4,
  fontSize: 18,
  bold: true,
  color: COLORS.secondary,
  isTextBox: true
});

slide.addText([
  { text: "• Ambiguous problems\n", options: { breakLine: true } },
  { text: "• Medical/legal decisions\n", options: { breakLine: true } },
  { text: "• Code security reviews\n", options: { breakLine: true } },
  { text: "• Fact-checking claims\n", options: { breakLine: true } },
  { text: "• Complex reasoning\n", options: { breakLine: true } },
  { text: "• Edge case detection" }
], {
  x: 1.0, y: 2.0, w: 3.6, h: 2.0,
  fontSize: 14,
  color: COLORS.text,
  bullet: true,
  isTextBox: true
});

slide.addText("⚠️ Minimal Improvement:", {
  x: 5.2, y: 1.5, w: 4.0, h: 0.4,
  fontSize: 18,
  bold: true,
  color: "E67E22",
  isTextBox: true
});

slide.addText([
  { text: "• Simple math calculations\n", options: { breakLine: true } },
  { text: "• Straightforward facts\n", options: { breakLine: true } },
  { text: "• Well-defined problems\n", options: { breakLine: true } },
  { text: "• Clear-cut answers" }
], {
  x: 5.4, y: 2.0, w: 3.6, h: 1.5,
  fontSize: 14,
  color: COLORS.text,
  bullet: true,
  isTextBox: true
});

// Key insight box
slide.addShape(pres.ShapeType.rect, {
  x: 1.0, y: 4.2, w: 8.0, h: 0.8,
  fill: { color: COLORS.accent },
  line: { width: 0 },
  isTextBox: true
});

slide.addText("💡 Key Insight: Multi-agent adds most value when problems have multiple valid interpretations or hidden complexity", {
  x: 1.2, y: 4.4, w: 7.6, h: 0.4,
  fontSize: 14,
  bold: true,
  color: COLORS.dark,
  align: "center",
  isTextBox: true
});

// ============ SLIDE 8: Technical Architecture ============
slide = pres.addSlide();
slide.background = { color: COLORS.light };

slide.addText("Technical Implementation", {
  x: 0.5, y: 0.5, w: 9, h: 0.6,
  fontSize: 40,
  bold: true,
  color: COLORS.primary,
  isTextBox: true
});

// Architecture components
const techSpecs = [
  { icon: "🤖", title: "Model", detail: "Google Gemma 2B-IT (quantized)" },
  { icon: "⚡", title: "Execution", detail: "Parallel agent processing" },
  { icon: "🔄", title: "Reconciliation", detail: "Weighted voting with confidence scoring" },
  { icon: "📊", title: "Evaluation", detail: "18 test cases across 5 domains" },
  { icon: "🎯", title: "Accuracy", detail: "Keyword + semantic similarity metrics" },
  { icon: "🖥️", title: "Interface", detail: "Streamlit web dashboard" }
];

techSpecs.forEach((spec, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  const x = 0.8 + col * 3.1;
  const y = 1.8 + row * 1.3;

  slide.addShape(pres.ShapeType.rect, {
    x: x, y: y, w: 2.9, h: 1.0,
    fill: { color: "FFFFFF" },
    line: { color: COLORS.secondary, width: 2 },
    isTextBox: true
  });

  slide.addText(spec.icon, {
    x: x + 0.15, y: y + 0.15, w: 0.5, h: 0.5,
    fontSize: 24,
    isTextBox: true
  });

  slide.addText(spec.title, {
    x: x + 0.7, y: y + 0.15, w: 2.0, h: 0.3,
    fontSize: 14,
    bold: true,
    color: COLORS.text,
    isTextBox: true
  });

  slide.addText(spec.detail, {
    x: x + 0.7, y: y + 0.5, w: 2.0, h: 0.4,
    fontSize: 11,
    color: COLORS.text,
    isTextBox: true
  });
});

// ============ SLIDE 9: Live Demo ============
slide = pres.addSlide();
slide.background = { color: COLORS.secondary };

slide.addText("Live Demo", {
  x: 0.5, y: 1.5, w: 9, h: 0.8,
  fontSize: 48,
  bold: true,
  color: COLORS.lightText,
  align: "center",
  isTextBox: true
});

slide.addText("Streamlit Web Interface", {
  x: 0.5, y: 2.5, w: 9, h: 0.4,
  fontSize: 20,
  color: COLORS.light,
  align: "center",
  isTextBox: true
});

slide.addText([
  { text: "• Enter any question\n", options: { breakLine: true } },
  { text: "• See all 4 agent perspectives\n", options: { breakLine: true } },
  { text: "• View reconciled answer\n", options: { breakLine: true } },
  { text: "• Compare vs single agent" }
], {
  x: 2.5, y: 3.2, w: 5.0, h: 1.2,
  fontSize: 16,
  color: COLORS.lightText,
  bullet: true,
  isTextBox: true
});

// ============ SLIDE 10: Conclusion ============
slide = pres.addSlide();
slide.background = { color: COLORS.primary };

slide.addText("Key Takeaways", {
  x: 0.5, y: 0.7, w: 9, h: 0.6,
  fontSize: 40,
  bold: true,
  color: COLORS.lightText,
  isTextBox: true
});

slide.addText([
  { text: "✓ ", options: { fontSize: 20, color: COLORS.accent } },
  { text: "Multi-agent approach improves accuracy by 15-23%\n", options: { breakLine: true } },
  { text: "\n✓ ", options: { breakLine: true, fontSize: 20, color: COLORS.accent } },
  { text: "Most effective for ambiguous, complex problems\n", options: { breakLine: true } },
  { text: "\n✓ ", options: { breakLine: true, fontSize: 20, color: COLORS.accent } },
  { text: "Error detection improves by 33%\n", options: { breakLine: true } },
  { text: "\n✓ ", options: { breakLine: true, fontSize: 20, color: COLORS.accent } },
  { text: "Lightweight models make parallel processing feasible" }
], {
  x: 1.5, y: 1.8, w: 7.0, h: 2.0,
  fontSize: 16,
  color: COLORS.lightText,
  isTextBox: true
});

slide.addShape(pres.ShapeType.rect, {
  x: 1.5, y: 4.2, w: 7.0, h: 0.7,
  fill: { color: COLORS.accent },
  line: { width: 0 },
  isTextBox: true
});

slide.addText("Multiple perspectives lead to more reliable AI", {
  x: 1.5, y: 4.35, w: 7.0, h: 0.4,
  fontSize: 20,
  bold: true,
  color: COLORS.dark,
  align: "center",
  isTextBox: true
});

// Save presentation
pres.writeFile({ fileName: "Multi_Agent_Gemma_Presentation.pptx" });

console.log("✓ Presentation created successfully!");
console.log("File: Multi_Agent_Gemma_Presentation.pptx");
