"""
报告生成引擎

生成 HTML 分析报告
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class ReportEngine:
    """报告生成引擎"""

    def __init__(self):
        """初始化引擎"""
        self.template = None

    def generate_html_report(
        self, results: Dict[str, Any], output_path: Optional[str] = None
    ) -> str:
        """生成 HTML 报告

        Args:
            results: 模拟结果
            output_path: 输出路径

        Returns:
            str: HTML 报告内容
        """
        html = self._generate_header()
        html += self._generate_summary(results)
        html += self._generate_parameters(results)
        html += self._generate_results(results)
        html += self._generate_errors(results)
        html += self._generate_footer()

        if output_path:
            Path(output_path).write_text(html, encoding="utf-8")

        return html

    def _generate_header(self) -> str:
        """生成报告头部"""
        return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CFD-Class 模拟报告</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .success {
            color: #27ae60;
            font-weight: bold;
        }
        .error {
            color: #e74c3c;
            font-weight: bold;
        }
        .info {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌊 CFD-Class 模拟报告</h1>
"""

    def _generate_summary(self, results: Dict[str, Any]) -> str:
        """生成摘要部分"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""
        <h2>📋 报告摘要</h2>
        <div class="info">
            <p><strong>生成时间:</strong> {timestamp}</p>
            <p><strong>软件版本:</strong> CFD-Class v0.1.0-alpha</p>
            <p><strong>模拟状态:</strong> <span class="{'success' if results.get('success') else 'error'}">{'成功' if results.get('success') else '失败'}</span></p>
        </div>
"""
        return html

    def _generate_parameters(self, results: Dict[str, Any]) -> str:
        """生成参数部分"""
        config = results.get("config")
        if not config:
            return ""

        html = """
        <h2>⚙️ 物理参数</h2>
        <table>
            <tr>
                <th>参数</th>
                <th>值</th>
                <th>单位</th>
            </tr>
"""

        params = [
            ("Domain Length", getattr(config, "domain_length", "N/A"), "m"),
            ("Grid Points", getattr(config, "nx", "N/A"), ""),
            ("Dam Position", getattr(config, "_x_dam", "N/A"), "m"),
            ("Left Depth", getattr(config, "h_l", "N/A"), "m"),
            ("Right Depth", getattr(config, "h_r", "N/A"), "m"),
            ("Left Velocity", getattr(config, "u_l", "N/A"), "m/s"),
            ("Right Velocity", getattr(config, "u_r", "N/A"), "m/s"),
            ("Gravity", getattr(config, "g", "N/A"), "m/s²"),
            ("End Time", getattr(config, "t_end", "N/A"), "s"),
            ("CFL Number", getattr(config, "cfl", "N/A"), ""),
        ]

        for name, value, unit in params:
            html += f"""
            <tr>
                <td>{name}</td>
                <td>{value}</td>
                <td>{unit}</td>
            </tr>
"""

        html += "</table>"
        return html

    def _generate_results(self, results: Dict[str, Any]) -> str:
        """生成结果部分"""
        schemes = results.get("schemes", {})

        if not schemes:
            return ""

        html = """
        <h2>📊 模拟结果</h2>
        <table>
            <tr>
                <th>格式</th>
                <th>状态</th>
                <th>说明</th>
            </tr>
"""

        for scheme_name in schemes.keys():
            html += f"""
            <tr>
                <td>{scheme_name}</td>
                <td><span class="success">✅ 完成</span></td>
                <td>模拟成功完成</td>
            </tr>
"""

        html += "</table>"
        return html

    def _generate_errors(self, results: Dict[str, Any]) -> str:
        """生成误差部分"""
        errors = results.get("errors", {})

        if not errors:
            return ""

        html = """
        <h2>📈 误差分析</h2>
        <table>
            <tr>
                <th>格式</th>
                <th>L1 误差</th>
                <th>L2 误差</th>
                <th>L∞ 误差</th>
            </tr>
"""

        for scheme_name, error_data in errors.items():
            if "error" in error_data:
                html += f"""
            <tr>
                <td>{scheme_name}</td>
                <td colspan="3"><span class="error">❌ {error_data['error']}</span></td>
            </tr>
"""
            else:
                l1_val = error_data.get("l1", None)
                l2_val = error_data.get("l2", None)
                linf_val = error_data.get("linf", None)

                l1_str = f"{l1_val:.6f}" if l1_val is not None else "N/A"
                l2_str = f"{l2_val:.6f}" if l2_val is not None else "N/A"
                linf_str = f"{linf_val:.6f}" if linf_val is not None else "N/A"

                html += f"""
            <tr>
                <td>{scheme_name}</td>
                <td>{l1_str}</td>
                <td>{l2_str}</td>
                <td>{linf_str}</td>
            </tr>
"""

        html += "</table>"
        return html

    def _generate_footer(self) -> str:
        """生成报告底部"""
        return """
        <div class="footer">
            <p>Generated by CFD-Class | 符合GB/T国标的计算流体动力学教学软件</p>
            <p><a href="https://github.com/kaklos-cyber/cfd_class">GitHub Repository</a></p>
        </div>
    </div>
</body>
</html>
"""
