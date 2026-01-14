import sys
import os
import time
import json
import base64
import platform
import pyperclip
import subprocess
from pathlib import Path
from pynput import keyboard
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QSystemTrayIcon, 
                             QMenu, QHBoxLayout, QMessageBox, QListWidget, QListWidgetItem,
                             QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QIcon, QAction, QColor, QPalette, QFont, QPixmap

ICON_DATA = """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"""

def get_embedded_icon():
    try:
        data = base64.b64decode(ICON_DATA)
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        return QIcon(pixmap)
    except Exception:
        return QIcon()

def enable_drag_drop_as_admin():
    """
    尝试绕过 Windows UIPI 限制，允许管理员权限下接收文件拖拽消息。
    """
    if platform.system() != 'Windows':
        return

    import ctypes
    try:
        WM_DROPFILES = 0x0233
        WM_COPYDATA = 0x004A
        WM_COPYGLOBALDATA = 0x0049
        MSGFLT_ADD = 1
        
        lib = ctypes.windll.user32
        lib.ChangeWindowMessageFilter(WM_DROPFILES, MSGFLT_ADD)
        lib.ChangeWindowMessageFilter(WM_COPYDATA, MSGFLT_ADD)
        lib.ChangeWindowMessageFilter(WM_COPYGLOBALDATA, MSGFLT_ADD)
    except Exception:
        pass

class FloatingWindow(QWidget):
    def __init__(self, main_window):
        super().__init__(None)
        self.main_window = main_window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.WindowStaysOnTopHint | 
                            Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        self.container = QFrame()
        self.container.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 30, 220);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 30);
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 0)
        self.container.setGraphicsEffect(shadow)
        
        container_layout = QVBoxLayout(self.container)
        
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.info_label.setStyleSheet("border: none; background: transparent;")
        self.update_content("等待开始", "...")
        
        container_layout.addWidget(self.info_label)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(5)
        
        self.prev_btn = QPushButton("◀")
        self.prev_btn.setFixedSize(24, 24)
        self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prev_btn.setStyleSheet(self._mini_btn_style())
        self.prev_btn.setToolTip("上一条")
        self.prev_btn.clicked.connect(self.main_window.prev_item)
        
        self.reset_btn = QPushButton("↺")
        self.reset_btn.setFixedSize(24, 24)
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.setStyleSheet(self._mini_btn_style(is_warning=True))
        self.reset_btn.setToolTip("重置进度")
        self.reset_btn.clicked.connect(self.main_window.reset_progress)
        
        self.next_btn = QPushButton("▶")
        self.next_btn.setFixedSize(24, 24)
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.setStyleSheet(self._mini_btn_style())
        self.next_btn.setToolTip("下一条")
        self.next_btn.clicked.connect(self.main_window.next_item)
        
        self.lock_btn = QPushButton("🔓")
        self.lock_btn.setFixedSize(24, 24)
        self.lock_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lock_btn.setStyleSheet(self._mini_btn_style())
        self.lock_btn.setToolTip("锁定位置 (拖动禁用)")
        self.lock_btn.clicked.connect(self.toggle_lock)
        
        btn_layout.addWidget(self.prev_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addWidget(self.next_btn)
        btn_layout.addWidget(self.lock_btn)
        container_layout.addLayout(btn_layout)

        self.layout.addWidget(self.container)

        self.setFixedSize(200, 115)
        self.is_hidden = False
        self.is_locked = False
        self.edge_margin = 5
        
        self.setWindowIcon(get_embedded_icon())
        
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_edge)
        self.check_timer.start(200)

    def get_screen_rect(self):
        center = self.geometry().center()
        screen = QApplication.screenAt(center)
        if not screen:
            min_dist = float('inf')
            best_screen = QApplication.primaryScreen()
            for s in QApplication.screens():
                s_center = s.geometry().center()
                dist = (s_center.x() - center.x())**2 + (s_center.y() - center.y())**2
                if dist < min_dist:
                    min_dist = dist
                    best_screen = s
            return best_screen.geometry()
        return screen.geometry()

    def trigger_startup_hint(self):
        self.hide_block_until = time.time() + 20
        self.is_hidden = False
        
        screen_rect = self.get_screen_rect()
        window_rect = self.geometry()
        
        target_x = window_rect.x()
        
        if window_rect.right() > screen_rect.right() - 15:
            target_x = screen_rect.right() - self.width()
            
        elif window_rect.left() < screen_rect.left() + 15:
            target_x = screen_rect.left()
            
        if target_x != window_rect.x():
            self.move(target_x, window_rect.y())

    def _mini_btn_style(self, is_warning=False):
        hover_color = "rgba(255, 100, 100, 80)" if is_warning else "rgba(255, 255, 255, 60)"
        return f"""
            QPushButton {{
                background-color: rgba(255, 255, 255, 30);
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: rgba(255, 255, 255, 90);
            }}
        """

    def update_content(self, current_text, next_text):
        def truncate(text, length=10):
            return (text[:length] + '..') if len(text) > length else text
            
        html = f"""
        <div style='line-height: 1.4;'>
            <span style='font-size: 10px; color: #aaaaaa;'>当前:</span><br>
            <span style='font-size: 14px; font-weight: bold; color: #ffffff;'>{truncate(current_text, 12)}</span><br>
            <div style='height: 4px;'></div>
            <span style='font-size: 9px; color: #888888;'>下条: {truncate(next_text, 15)}</span>
        </div>
        """
        self.info_label.setText(html)

    def check_edge(self):
        if not self.isVisible() or self.animation.state() == QPropertyAnimation.State.Running:
            return
            
        if hasattr(self, 'hide_block_until') and time.time() < self.hide_block_until:
            return
            
        cursor_pos = self.cursor().pos()
        window_rect = self.geometry()
        screen_rect = self.get_screen_rect()
        
        should_show = False
        
        if self.is_hidden:
            vertical_range = (cursor_pos.y() >= window_rect.top() - 20) and \
                           (cursor_pos.y() <= window_rect.bottom() + 20)
            
            if vertical_range:
                if window_rect.left() < screen_rect.left():
                    if cursor_pos.x() < screen_rect.left() + 20:
                        should_show = True
                elif window_rect.right() > screen_rect.right():
                    if cursor_pos.x() > screen_rect.right() - 20:
                        should_show = True
        else:
            in_window = window_rect.adjusted(-20, -20, 20, 20).contains(cursor_pos)
            if not in_window:
                if window_rect.right() >= screen_rect.right() - self.edge_margin:
                    self.hide_to_edge('right', screen_rect.right())
                elif window_rect.left() <= screen_rect.left() + self.edge_margin:
                    self.hide_to_edge('left', screen_rect.left())
            return

        if should_show:
            self.show_from_edge()

    def hide_to_edge(self, edge, pos):
        if self.is_hidden: return
        self.is_hidden = True
        
        if edge == 'right':
            target_pos = QPoint(pos - 15, self.y())
        else:
            target_pos = QPoint(pos - self.width() + 15, self.y())
            
        self.animation.setEndValue(target_pos)
        self.animation.start()

    def show_from_edge(self):
        if not self.is_hidden: return
        self.is_hidden = False
        screen_rect = self.get_screen_rect()
        
        if self.x() + self.width() / 2 > screen_rect.center().x():
            target_x = screen_rect.right() - self.width()
        else:
            target_x = screen_rect.left()
            
        self.animation.setEndValue(QPoint(target_x, self.y()))
        self.animation.start()

    def toggle_lock(self):
        self.is_locked = not self.is_locked
        if self.is_locked:
            self.lock_btn.setText("🔒")
            self.lock_btn.setToolTip("位置已锁定 (点击解锁)")
            self.lock_btn.setStyleSheet(self._mini_btn_style(is_warning=True))
        else:
            self.lock_btn.setText("🔓")
            self.lock_btn.setToolTip("锁定位置 (拖动禁用)")
            self.lock_btn.setStyleSheet(self._mini_btn_style())

    def mousePressEvent(self, event):
        if self.is_locked:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_locked:
            return
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("顺序粘贴工具")
        self.setMinimumSize(400, 500)
        
        self.items = []
        self.index = 0
        self.os_type = platform.system()
        self.ctrl_pressed = False
        self.cmd_pressed = False
        self.shift_pressed = False
        self.alt_pressed = False
        
        if self.os_type == 'Windows':
            app_data = os.environ.get('APPDATA')
            base_dir = app_data if app_data else os.path.expanduser('~')
            config_dir = os.path.join(base_dir, 'SequentialPasteTool')
        elif self.os_type == 'Darwin':
            config_dir = os.path.expanduser('~/Library/Application Support/SequentialPasteTool')
        else:
            config_dir = os.path.expanduser('~/.config/SequentialPasteTool')
            
        if not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir)
            except Exception:
                config_dir = os.path.expanduser('~')

        self.config_file = os.path.join(config_dir, "config.json")
        
        self.init_ui()
        self.init_tray()
        self.init_keyboard()

        enable_drag_drop_as_admin()
        self.setAcceptDrops(True)
        self.setWindowIcon(get_embedded_icon())
        
        self.floating_win = FloatingWindow(self)
        self.load_config()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        status_layout = QHBoxLayout()
        self.status_icon = QLabel("📋") 
        self.status_icon.setStyleSheet("font-size: 24px;")
        
        self.status_label = QLabel("准备就绪")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        
        status_layout.addWidget(self.status_icon)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        main_layout.addLayout(status_layout)
        
        list_label = QLabel("粘贴内容列表 (双击跳转):")
        list_label.setStyleSheet("color: #666; font-size: 12px;")
        main_layout.addWidget(list_label)
        
        self.list_widget = QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
                font-size: 13px;
            }
            QListWidget::item {
                height: 28px;
                padding-left: 5px;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #e0e0e0;
            }
        """)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        main_layout.addWidget(self.list_widget)
        
        control_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton("◀ 上一条")
        self.prev_btn.clicked.connect(self.prev_item)
        
        self.next_btn = QPushButton("下一条 ▶")
        self.next_btn.clicked.connect(self.next_item)
        
        self.reset_btn = QPushButton("↺ 重置")
        self.reset_btn.clicked.connect(self.reset_progress)
        
        control_layout.addWidget(self.prev_btn)
        control_layout.addWidget(self.reset_btn)
        control_layout.addWidget(self.next_btn)
        main_layout.addLayout(control_layout)
        
        settings_group = QFrame()
        settings_group.setStyleSheet(".QFrame { background-color: #f0f0f0; border-radius: 5px; }")
        settings_layout = QHBoxLayout(settings_group)
        settings_layout.setContentsMargins(10, 10, 10, 10)
        
        self.import_btn = QPushButton("📂 导入文件")
        self.import_btn.clicked.connect(self.import_file)
        
        self.toggle_float_btn = QPushButton("🖥️ 开启悬浮窗")
        self.toggle_float_btn.setCheckable(True)
        self.toggle_float_btn.clicked.connect(self.toggle_floating)
        
        self.autostart_btn = QPushButton("🚀 开机自启")
        self.autostart_btn.setCheckable(True)
        self.autostart_btn.setChecked(self.is_autostart_enabled())
        self.autostart_btn.clicked.connect(self.toggle_autostart)

        self.background_btn = QPushButton("🕶️ 后台运行")
        self.background_btn.clicked.connect(self.hide_to_tray)
        
        for btn in [self.import_btn, self.toggle_float_btn, self.autostart_btn, self.background_btn,
                   self.prev_btn, self.next_btn, self.reset_btn]:
            if not btn.styleSheet():
                btn.setStyleSheet("""
                    QPushButton {
                        padding: 6px 12px;
                        border-radius: 4px;
                        background-color: #ffffff;
                        border: 1px solid #cccccc;
                    }
                    QPushButton:hover {
                        background-color: #e6f1ff;
                        border-color: #0078d7;
                    }
                    QPushButton:checked {
                        background-color: #cce4f7;
                        border-color: #005a9e;
                    }
                    QPushButton:pressed {
                        background-color: #c0dcf5;
                    }
                """)
        
        settings_layout.addWidget(self.import_btn)
        settings_layout.addWidget(self.toggle_float_btn)
        settings_layout.addWidget(self.autostart_btn)
        settings_layout.addWidget(self.background_btn)
        main_layout.addWidget(settings_group)
        
        tip_label = QLabel("提示：按 Ctrl+V 依次粘贴，Alt+Ctrl+V 回退，也可直接拖入TXT文件")
        tip_label.setStyleSheet("color: #888; font-size: 11px; margin-top: 5px;")
        tip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(tip_label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith('.txt'):
                    event.accept()
                    return
        event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls() if u.toLocalFile().lower().endswith('.txt')]
        if files:
            self.load_items(files[0])

    def load_items(self, file_path):
        try:
            self.current_file = file_path
            with open(file_path, "r", encoding="utf-8") as f:
                self.items = [line.strip() for line in f.readlines() if line.strip()]
            
            self.list_widget.clear()
            for i, item in enumerate(self.items):
                list_item = QListWidgetItem(f"{i+1}. {item}")
                self.list_widget.addItem(list_item)
            
            self.index = 0
            self.update_ui_state()
            self.status_label.setText(f"已导入 {len(self.items)} 项")
            
            if self.items:
                pyperclip.copy(self.items[0])
        except Exception as e:
            QMessageBox.critical(self, "导入失败", str(e))

    def is_autostart_enabled(self):
        if self.os_type == 'Windows':
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
                winreg.QueryValueEx(key, "SequentialPasteTool")
                return True
            except: return False
        elif self.os_type == 'Darwin':
            return os.path.exists(os.path.expanduser("~/Library/LaunchAgents/com.sequentialpaste.tool.plist"))
        else:
            return os.path.exists(os.path.expanduser("~/.config/autostart/sequential_paste.desktop"))

    def toggle_autostart(self):
        enabled = self.autostart_btn.isChecked()
        app_path = os.path.abspath(sys.argv[0])
        
        if self.os_type == 'Windows':
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
            if enabled:
                winreg.SetValueEx(key, "SequentialPasteTool", 0, winreg.REG_SZ, app_path)
            else:
                try: winreg.DeleteValue(key, "SequentialPasteTool")
                except: pass
        elif self.os_type == 'Darwin':
            plist_path = os.path.expanduser("~/Library/LaunchAgents/com.sequentialpaste.tool.plist")
            if enabled:
                plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sequentialpaste.tool</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{app_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>"""
                with open(plist_path, "w") as f: f.write(plist_content)
            else:
                if os.path.exists(plist_path): os.remove(plist_path)
        else: 
            autostart_dir = os.path.expanduser("~/.config/autostart/")
            os.makedirs(autostart_dir, exist_ok=True)
            desktop_file = os.path.join(autostart_dir, "sequential_paste.desktop")
            if enabled:
                content = f"""[Desktop Entry]
Type=Application
Exec={sys.executable} "{app_path}"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Sequential Paste Tool
Comment=Auto-paste tool
"""
                with open(desktop_file, "w") as f: f.write(content)
            else:
                if os.path.exists(desktop_file): os.remove(desktop_file)
        
        self.status_label.setText(f"自启已{'开启' if enabled else '关闭'}")

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(get_embedded_icon()) 
        
        tray_menu = QMenu()
        show_action = QAction("显示主界面", self)
        show_action.triggered.connect(self.show)
        
        float_action = QAction("切换悬浮窗", self)
        float_action.triggered.connect(self.toggle_floating)
        
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(float_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.on_tray_activated)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.showNormal()
            self.activateWindow()

    def toggle_floating(self):
        if self.floating_win.isVisible():
            self.floating_win.hide()
            self.toggle_float_btn.setText("🖥️ 开启悬浮窗")
            self.toggle_float_btn.setChecked(False)
        else:
            self.floating_win.show()
            self.floating_win.trigger_startup_hint()
            self.toggle_float_btn.setText("🖥️ 关闭悬浮窗")
            self.toggle_float_btn.setChecked(True)

    def hide_to_tray(self):
        if self.tray_icon.isVisible():
            self.hide()
            self.tray_icon.showMessage(
                "顺序粘贴工具",
                "程序已在后台运行，点击托盘图标可恢复",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )

    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                last_file = config.get('last_file', '')
                if last_file and os.path.exists(last_file):
                    self.load_items(last_file)
                    self.index = config.get('index', 0)
                    if self.index >= len(self.items):
                        self.index = 0
                    self.update_ui_state()
                
                if config.get('floating_visible', False):
                    self.toggle_floating()
                    
                if config.get('floating_locked', False):
                    if not self.floating_win.is_locked:
                        self.floating_win.toggle_lock()
                
                fx = config.get('floating_x')
                fy = config.get('floating_y')
                if fx is not None and fy is not None:
                    self.floating_win.move(fx, fy)
                    self.floating_win.trigger_startup_hint()
        except Exception:
            pass

    def save_config(self):
        try:
            config_dir = os.path.dirname(self.config_file)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)

            config = {
                'last_file': self.current_file if hasattr(self, 'current_file') else '',
                'index': self.index,
                'floating_visible': self.floating_win.isVisible(),
                'floating_locked': self.floating_win.is_locked,
                'floating_x': self.floating_win.pos().x(),
                'floating_y': self.floating_win.pos().y()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f)
        except Exception:
            pass

    def closeEvent(self, event):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('退出确认')
        msg_box.setText("是否最小化到托盘运行？")
        msg_box.setIcon(QMessageBox.Icon.Question)
        
        minimize_btn = msg_box.addButton("最小化到托盘", QMessageBox.ButtonRole.YesRole)
        quit_btn = msg_box.addButton("直接退出", QMessageBox.ButtonRole.NoRole)
        cancel_btn = msg_box.addButton("取消", QMessageBox.ButtonRole.RejectRole)
        
        msg_box.exec()
        
        clicked = msg_box.clickedButton()
        if clicked == minimize_btn:
            event.ignore()
            self.hide_to_tray()
            self.save_config()
        elif clicked == quit_btn:
            self.save_config()
            event.accept()
            QApplication.instance().quit()
        else:
            event.ignore()

    def import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文本文件", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.load_items(file_path)

    def on_item_double_clicked(self, item):
        row = self.list_widget.row(item)
        self.index = row
        self.update_ui_state()
        self.status_label.setText(f"跳转至第 {row + 1} 项")

    def reset_progress(self):
        if not self.items: return
        self.index = 0
        self.update_ui_state()
        self.status_label.setText("进度已重置")

    def prev_item(self):
        if not self.items: return
        if self.index > 0:
            self.index -= 1
            self.update_ui_state()
            self.status_label.setText(f"回退至: {self.items[self.index]}")

    def next_item(self):
        if not self.items: return
        if self.index < len(self.items) - 1:
            self.index += 1
            self.update_ui_state()
            self.status_label.setText(f"前进至: {self.items[self.index]}")
        elif self.index == len(self.items) - 1:
            self.index += 1
            self.update_ui_state()
            self.status_label.setText("已到达列表末尾")

    def update_ui_state(self):
        if not self.items:
            return
        if self.index >= len(self.items):
            current_text = "已结束"
            next_text = "-"
            self.list_widget.setCurrentItem(None)
        else:
            current_text = self.items[self.index]
            next_text = self.items[self.index + 1] if self.index + 1 < len(self.items) else "无 (结束)"
            self.list_widget.setCurrentRow(self.index)
            self.list_widget.scrollToItem(self.list_widget.item(self.index))
            try:
                pyperclip.copy(current_text)
            except Exception:
                QTimer.singleShot(100, lambda: pyperclip.copy(current_text))

        if self.floating_win:
            self.floating_win.update_content(current_text, next_text)
        self.setWindowTitle(f"顺序粘贴工具 - {self.index + 1}/{len(self.items)}")

    def update_clipboard(self):
        if self.index < len(self.items):
            self.next_item()

    def init_keyboard(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        if key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            self.ctrl_pressed = True
            return
        if key == keyboard.Key.cmd or key == keyboard.Key.cmd_l or key == keyboard.Key.cmd_r:
            self.cmd_pressed = True
            return
        if key == keyboard.Key.shift or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
            self.shift_pressed = True
            return
        if key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            self.alt_pressed = True
            return
        if not (self.ctrl_pressed or self.cmd_pressed):
            return

        try:
            is_v_pressed = False
            if hasattr(key, 'char') and key.char:
                if key.char.lower() == 'v':
                    is_v_pressed = True
                elif key.char == '\x16':
                    is_v_pressed = True
            
            if not is_v_pressed and hasattr(key, 'vk') and key.vk:
                if self.os_type == 'Darwin':
                    if key.vk == 9: 
                        is_v_pressed = True
                else:
                    if key.vk == 86:
                        is_v_pressed = True

            if is_v_pressed:
                is_control_down = (self.os_type == 'Darwin' and self.cmd_pressed) or \
                                  (self.os_type != 'Darwin' and self.ctrl_pressed)
                
                if is_control_down:
                    if self.alt_pressed:
                        QTimer.singleShot(0, self.prev_item)
                    elif not self.shift_pressed:
                        QTimer.singleShot(100, self.update_clipboard)
                        
        except Exception as e:
            pass

    def on_release(self, key):
        if key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            self.ctrl_pressed = False
        elif key == keyboard.Key.cmd or key == keyboard.Key.cmd_l or key == keyboard.Key.cmd_r:
            self.cmd_pressed = False
        elif key == keyboard.Key.shift or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
            self.shift_pressed = False
        elif key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            self.alt_pressed = False

    def check_permissions(self):
        if self.os_type == 'Darwin':
            try:
                from pynput import keyboard
                self.status_label.setText("macOS: 请确保辅助功能权限已开启")
            except Exception as e:
                self.status_label.setText(f"权限检查失败: {e}")
        elif self.os_type == 'Windows':
            import ctypes
            try:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                if not is_admin:
                    self.status_label.setText("⚠️ 建议以管理员运行 (避免快捷键失效)")
                    self.status_label.setStyleSheet("color: #d9534f; font-weight: bold;")
                else:
                    self.status_label.setText("✅ 管理员权限已就绪")
                    self.status_label.setStyleSheet("color: green; font-weight: bold;")
            except:
                self.status_label.setText("Windows 权限检查异常")
        else:
            self.status_label.setText("Linux: 需确保输入设备访问权限")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    enable_drag_drop_as_admin()
    app.setQuitOnLastWindowClosed(False)
    
    font = QFont("Segoe UI", 9) if platform.system() == "Windows" else QFont("Helvetica Neue", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.check_permissions()
    window.show()
    sys.exit(app.exec())