

class Memory:
    def __init__(self):
        self.pids = dict()
        self.length = 1

    def add_var(self, pid):
        if pid in self.pids.keys():
            return False
        else:
            self.pids[pid] = [self.length, -1, "var"]
            self.length += 1
            return True

    def add_tab(self, pid, s, e):
        if pid in self.pids.keys() or e < s:
            return False
        else:
            self.pids[pid] = [self.length, s, "tab"]
            self.length += e - s + 1
            return True

    def initialize_var(self, pid):
        if pid in self.pids.keys():
            self.pids[pid][1] = 0
            return True
        else:
            return False

    def check_var(self, pid):
        if pid in self.pids.keys():
            if self.pids[pid][1] == 0:
                return True    
        return False

    def get_var(self, pid):
        if pid in self.pids.keys():
            i = self.pids[pid]
            if i[2] != "var":
                return -2
            return i[0]
        else:
            return -1

    def get_tab(self, pid, index):
        if pid in self.pids.keys():
            i = self.pids[pid]
            if i[2] != "tab":
                return -2
            return i[0] + index - i[1]
        else:
            return -1

    def get_tab_var(self, pid):
        if pid in self.pids.keys():
            i = self.pids[pid]
            if i[2] != "tab":
                return -2
            return i[0:2]
        else:
            return -1

    def rm_var(self, pid):
        if pid in self.pids.keys():
            del self.pids[pid]
            return True
        else:
            return false
