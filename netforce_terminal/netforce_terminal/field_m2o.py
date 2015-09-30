# Copyright (c) 2012-2015 Netforce Co. Ltd.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

from netforce_terminal.view import NFView,make_view
from netforce_terminal.utils import filter_chars
from netforce.database import Transaction
from netforce.model import get_model
import curses
import curses.textpad

class FieldM2O(NFView):
    _name="field_m2o"

    def __init__(self,opts):
        super().__init__(opts)
        self.key=opts["key"]
        self.relation=opts["relation"]
        self.condition=opts.get("condition")
        self.string=opts["string"]
        self.data=opts["data"]
        self.name=opts["name"]
        self.name_field=opts.get("name_field")
        self.readonly=opts.get("readonly")

    def render(self):
        self.win.clear()
        if self.readonly:
            self.win.addstr(0,0,"%s."%self.key)
        else:
            self.win.addstr(0,0,"%s."%self.key,curses.A_BOLD|curses.color_pair(2))
        val=self.data.get(self.name)
        if val:
            n=filter_chars(val[1][:20])
            self.win.addstr(0,3,"%s: %s"%(self.string,n))
        else:
            self.win.addstr(0,3,"Select %s"%self.string)
        self.win.refresh()

    def focus(self):
        opts={
            "model": self.relation,
            "condition": self.condition, 
        }
        v=make_view("select_item",opts)
        v.render()
        res=v.focus()
        with Transaction():
            if res:
                obj_id=res["select_id"]
                if obj_id:
                    if self.name_field:
                        n=get_model(self.relation).read([obj_id],[self.name_field])[0][self.name_field]
                    else:
                        n=get_model(self.relation).name_get([obj_id])[0][1]
                    val=(obj_id,n)
                else:
                    val=None
                self.data[self.name]=val

FieldM2O.register()
