class Symbol:
    """
    符号基类
    """
    def __init__(self, name):
        """
        构造
        :param name: 符号名
        """
        self.name = name


class SymbolTable:
    """
    符号表
    """
    def __init__(self):
        """
        构造
        """
        self._table = list()

    def exist(self, name):
        """
        给定名字的符号是否存在
        :param name:
        :return: True/False
        """
        for s in self._table:
            if s.name == name:
                return True
        return False

    def query(self, name):
        """
        查询特定名字的符号
        :param name: 名字
        :return: 符号
        """
        for symbol in self._table:
            if symbol.name == name:
                return symbol
        return None

    def append(self, symbol):
        """
        填入符号
        :param symbol: 符号
        """
        pass

    def num(self):
        """
        获取符号总数
        :return: 符号总数
        """
        return len(self._table)

    def get(self, index):
        """
        根据索引来获取符号
        :param index: 索引
        :return: 符号
        """
        return self._table[index]


class SymbolTablePool:
    """
    符号表池
    """
    def __init__(self):
        """
        构造
        """
        self.global_var_table = None
        self.local_var_tables = None
        self.fun_table = None

    def init(self):
        """
        初始化符号表池
        """
        self.global_var_table = GlobalVarTable()
        self.local_var_tables = list()
        self.fun_table = FunTable()

        # 添加 output 和 input 的支持
        self.local_var_tables.append(
            LocalVarTable('input', self.global_var_table)
        )
        self.local_var_tables.append(
            LocalVarTable('output', self.global_var_table)
        )
        self.query('output').append(
            LocalVar('num', 'int', 4, True)
        )
        self.fun_table.append(
            Fun('input', 'int', self.query('input'))
        )
        self.fun_table.append(
            Fun('output', 'void', self.query('output'))
        )

    def query(self, local_var_table_name):
        """
        查询局部变量表
        :param local_var_table_name: 表名
        :return: 局部变量表
        """
        for table in self.local_var_tables:
            if table.name == local_var_table_name:
                return table
        return None

    def append(self, local_var_table):
        """
        添加一张局部变量表
        :param local_var_table: 局部变量表
        """
        self.local_var_tables.append(local_var_table)


class GlobalVarTable(SymbolTable):
    """
    全局变量表
    """
    def __init__(self):
        """
        构造
        :param name:
        """
        super().__init__()
        self.__width = 0

    def append(self, symbol):
        """
        添加符号
        :param symbol: 符号
        """
        self._table.append(symbol)
        self._table[-1].offset = self.__width
        self.__width += self._table[-1].width


class GlobalVar(Symbol):
    """
    全局变量
    """
    def __init__(self, g_name, g_type, g_width):
        """
        全局变量
        :param g_name: 名字
        :param g_type: 类型
        :param g_width: 长度
        """
        super().__init__(g_name)
        self.type = g_type
        self.width = g_width


class LocalVarTable(SymbolTable):
    """
    局部变量表
    """
    def __init__(self, name, global_var_table):
        """
        构造
        :param name: 表名
        :param global_var_table 全局变量表
        """
        super().__init__()
        self.name = name
        self.outer = global_var_table
        self.__width = 0

    def append(self, symbol):
        """
        填入新符号
        :param symbol:
        """
        self._table.append(symbol)
        self._table[-1].offset = self.__width
        self.__width += self._table[-1].offset

    def exist(self, name):
        """
        是否已经存在
        :param name: 符号名
        :return: True/False
        """
        if self.outer.exist(name):
            return True
        else:
            for symbol in self._table:
                if symbol.name == name:
                    return True
            return False

    def get_params_num(self):
        """
        获取参数个数
        :return: 参数个数
        """
        num = 0
        for symbol in self._table:
            if symbol.is_param:
                num += 1
        return num

    def get_params(self):
        """
        获取参数列表
        :return: 参数列表
        """
        params = list()
        for symbol in self._table:
            if symbol.is_param:
                params.append(symbol)
        return params


class LocalVar(Symbol):
    """
    局部变量
    """
    def __init__(self, l_name, l_type, l_width, l_is_param):
        """
        构造
        :param l_name: 名字
        :param l_type: 类型
        :param l_width: 占空间
        :param l_is_param: 是否为参数
        """
        super().__init__(l_name)
        self.type = l_type
        self.width = l_width
        self.is_param = l_is_param


class FunTable(SymbolTable):
    """
    函数表
    """
    def __init__(self):
        """
        构造
        """
        super().__init__()

    def append(self, symbol):
        """
        填入一个新的函数
        :param symbol: 函数
        """
        self._table.append(symbol)


class Fun(Symbol):
    """
    函数
    """
    def __init__(self, name, return_type, local_var_table):
        """
        构造
        :param name: 函数名
        :param return_type: 返回类型
        :param local_var_table: 对应的局部变量表
        """
        super().__init__(name)
        self.param_types = list()
        self.return_type = return_type
        self.table = local_var_table
