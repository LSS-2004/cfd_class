"""
导航组件

提供页面导航和面包屑功能
"""

import streamlit as st
from typing import List, Dict, Optional


def render_navigation(
    current_page: str,
    pages: Optional[List[Dict[str, str]]] = None
) -> None:
    """渲染导航栏

    Args:
        current_page: 当前页面名称
        pages: 页面列表，每个页面包含 name 和 icon
    """
    if pages is None:
        pages = [
            {"name": "首页", "icon": "🏠", "page": "Home"},
            {"name": "模拟运行", "icon": "📊", "page": "Simulation"},
            {"name": "格式对比", "icon": "🔬", "page": "Comparison"},
            {"name": "理论背景", "icon": "📚", "page": "Theory"},
        ]

    # 创建导航栏
    cols = st.columns(len(pages))

    for idx, page in enumerate(pages):
        with cols[idx]:
            if page["page"] == current_page:
                st.markdown(
                    f"<div style='text-align: center; padding: 10px; "
                    f"background-color: #f0f2f6; border-radius: 10px; "
                    f"border: 2px solid #ff4b4b;'>"
                    f"<span style='font-size: 24px;'>{page['icon']}</span><br>"
                    f"<strong>{page['name']}</strong>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='text-align: center; padding: 10px; "
                    f"background-color: #f0f2f6; border-radius: 10px; "
                    f"cursor: pointer;'>"
                    f"<span style='font-size: 24px;'>{page['icon']}</span><br>"
                    f"{page['name']}"
                    f"</div>",
                    unsafe_allow_html=True
                )


def render_breadcrumb(path: List[str]) -> None:
    """渲染面包屑导航

    Args:
        path: 路径列表
    """
    breadcrumb = " > ".join(path)
    st.markdown(f"<small>{breadcrumb}</small>", unsafe_allow_html=True)


def render_page_header(
    title: str,
    subtitle: Optional[str] = None,
    icon: Optional[str] = None
) -> None:
    """渲染页面头部

    Args:
        title: 页面标题
        subtitle: 副标题
        icon: 图标
    """
    if icon:
        st.title(f"{icon} {title}")
    else:
        st.title(title)

    if subtitle:
        st.markdown(f"*{subtitle}*")

    st.divider()


def render_footer() -> None:
    """渲染页脚"""
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Made with ❤️ by CFD-Team | 符合GB/T国标的教学软件 | "
        "<a href='https://github.com/kaklos-cyber/cfd_class' target='_blank'>GitHub</a>"
        "</p>",
        unsafe_allow_html=True
    )
