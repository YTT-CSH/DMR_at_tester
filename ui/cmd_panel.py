# -*- coding: utf-8 -*-
"""指令树 + 参数表单 + 参数含义说明面板。"""
import tkinter as tk
from tkinter import ttk
from at_db import get_commands_by_group, is_command_for_model


class CmdPanel(ttk.PanedWindow):
    def __init__(self, master, comm, log_fn, **kw):
        super().__init__(master, orient=tk.HORIZONTAL, **kw)
        self.comm = comm
        self.log_fn = log_fn
        self.current_cmd = None
        self.param_widgets = []

        self._build_tree()
        self._build_form()
        self._build_explain()

        self.add(self.tree_frame, weight=1)
        self.add(self.form_frame, weight=2)
        self.add(self.explain_frame, weight=1)

        self._model = "通用(ALL)"
        self.refresh_tree()

    # ---------------- 左侧指令树 ----------------
    def _build_tree(self):
        self.tree_frame = ttk.Frame(self, width=200)
        self.tree = ttk.Treeview(self.tree_frame, show="tree", selectmode="browse")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        vsb = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree["yscrollcommand"] = vsb.set

    # ---------------- 中间参数表单 ----------------
    def _build_form(self):
        self.form_frame = ttk.Frame(self, width=420)
        # 标题
        self.title_var = tk.StringVar(value="请从左侧选择指令")
        self.title_lbl = tk.Label(self.form_frame, textvariable=self.title_var, font=("Microsoft YaHei", 11, "bold"))
        self.title_lbl.pack(anchor=tk.W, padx=8, pady=6)
        # 格式
        self.fmt_var = tk.StringVar()
        tk.Label(self.form_frame, textvariable=self.fmt_var, fg="blue", wraplength=400, justify=tk.LEFT).pack(anchor=tk.W, padx=8)
        # 参数容器
        self.param_area = tk.Frame(self.form_frame)
        self.param_area.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        # 按钮
        btn_frame = tk.Frame(self.form_frame)
        btn_frame.pack(anchor=tk.W, padx=8, pady=6)
        tk.Button(btn_frame, text="发送", width=10, bg="#4CAF50", fg="white", command=self._send).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="填充示例", width=10, command=self._fill_example).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="清空", width=10, command=self._clear_params).pack(side=tk.LEFT, padx=4)

    # ---------------- 右侧说明 ----------------
    def _build_explain(self):
        self.explain_frame = ttk.Frame(self, width=300)
        tk.Label(self.explain_frame, text="参数含义说明", font=("Microsoft YaHei", 10, "bold")).pack(anchor=tk.W, padx=8, pady=4)
        self.explain_txt = tk.Text(self.explain_frame, wrap=tk.WORD, state=tk.DISABLED, bg="#f7f7f7")
        self.explain_txt.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)

    # ---------------- 刷新指令树（按型号过滤） ----------------
    def set_model(self, model):
        self._model = model
        self.refresh_tree()

    def refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        grouped = get_commands_by_group()
        for group, cmds in grouped.items():
            visible = [c for c in cmds if is_command_for_model(c, self._model)]
            if not visible:
                continue
            g_node = self.tree.insert("", tk.END, text=f"{group} ({len(visible)})", open=True)
            for c in visible:
                self.tree.insert(g_node, tk.END, text=c["name"].replace("AT+", ""), values=[c["name"]])

    # ---------------- 选中指令 ----------------
    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = sel[0]
        values = self.tree.item(item, "values")
        if not values:  # 分组节点
            return
        name = values[0]
        cmd = self._find_cmd(name)
        if cmd:
            self._show_cmd(cmd)

    def _find_cmd(self, name):
        for g, cmds in get_commands_by_group().items():
            for c in cmds:
                if c["name"] == name:
                    return c
        return None

    def _show_cmd(self, cmd):
        self.current_cmd = cmd
        self.title_var.set(cmd["name"])
        self.fmt_var.set("格式: " + cmd["fmt"])
        self._clear_params()
        self.param_widgets = []

        if not cmd["params"]:
            tk.Label(self.param_area, text="（该指令无参数，可直接发送）", fg="gray").pack(anchor=tk.W, pady=6)
        else:
            for i, p in enumerate(cmd["params"]):
                row = tk.Frame(self.param_area)
                row.pack(fill=tk.X, pady=2)
                tk.Label(row, text=p["name"], width=14, anchor=tk.W).pack(side=tk.LEFT)
                # 固定字段（如保留位）显示为只读
                if "fixed" in p:
                    var = tk.StringVar(value=str(p["fixed"]))
                    ent = tk.Entry(row, textvariable=var, width=24, state=tk.DISABLED, disabledbackground="#eee")
                else:
                    var = tk.StringVar(value=str(p.get("default", "")))
                    ent = tk.Entry(row, textvariable=var, width=24)
                ent.pack(side=tk.LEFT, padx=4)
                # 范围/备注提示
                hint = p.get("range", "") if "fixed" not in p else p.get("note", "")
                tk.Label(row, text=hint, fg="#666", width=40, anchor=tk.W, wraplength=300).pack(side=tk.LEFT, padx=4)
                self.param_widgets.append((p, var, ent))

        self._update_explain(cmd)

    def _clear_params(self):
        for w in self.param_area.winfo_children():
            w.destroy()

    def _fill_example(self):
        if not self.current_cmd:
            return
        # 固定字段保持不动；可编辑字段填充推荐默认值（避免与协议示例错位）
        for (p, var, ent) in self.param_widgets:
            if "fixed" in p:
                continue
            var.set(str(p.get("default", "")))

    # ---------------- 构造并发送 ----------------
    def _send(self):
        if not self.current_cmd:
            return
        cmd = self.current_cmd
        # 无参数指令
        if not cmd["params"]:
            at_str = cmd["name"]
        else:
            vals = []
            ok = True
            for (p, var, ent) in self.param_widgets:
                v = var.get().strip()
                if v == "":
                    self.log_fn(f"[校验] 参数 {p['name']} 不能为空")
                    ent.config(bg="#ffdddd")
                    ok = False
                else:
                    ent.config(bg="white")
                    vals.append(v)
            if not ok:
                return
            at_str = cmd["name"] + "=" + ",".join(vals)
        resp = self.comm.send(at_str)
        if resp is None:
            if self.comm.is_open:
                self.log_fn("[提示] 指令已发送（无需应答或等待超时）")
            else:
                self.log_fn("[错误] 串口未连接")
        else:
            self.log_fn("[响应] " + resp)
            self._highlight_response(resp)

    def _highlight_response(self, resp):
        # 在说明区追加本次响应解析提示
        self.explain_txt.config(state=tk.NORMAL)
        self.explain_txt.insert(tk.END, f"\n--- 最近响应 ---\n{resp}\n")
        self.explain_txt.config(state=tk.DISABLED)
        self.explain_txt.see(tk.END)

    def _update_explain(self, cmd):
        self.explain_txt.config(state=tk.NORMAL)
        self.explain_txt.delete("1.0", tk.END)
        lines = []
        lines.append("【指令说明】")
        lines.append(cmd["desc"])
        lines.append("")
        lines.append("【参数含义】")
        if cmd["params"]:
            for p in cmd["params"]:
                lines.append(f"● {p['name']}：{p.get('note','')}")
                lines.append(f"    取值范围: {p.get('range','')}")
                if p.get("default") is not None:
                    lines.append(f"    默认值: {p['default']}")
        else:
            lines.append("（无参数）")
        lines.append("")
        lines.append("【响应格式】")
        lines.append(cmd["resp"])
        lines.append("")
        lines.append("【示例】")
        lines.append(cmd["example"])
        self.explain_txt.insert("1.0", "\n".join(lines))
        self.explain_txt.config(state=tk.DISABLED)
