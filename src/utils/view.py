from PyQt5.QtWidgets import *

def clearLayout(layout):
    for i in reversed(range(layout.count())):
        item = layout.itemAt(i)
        if isinstance(item, QWidgetItem):
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                layout.removeItem(item)
        elif isinstance(item, QLayoutItem):
            sub_layout = item.layout()
            if sub_layout is not None:
                clearLayout(sub_layout)
                layout.removeItem(item)
