import ast
import astunparse
import traceback
import json
from .model import AnyType, CompileOutput
from .errors import CompileError
from .utils import insert_returns


class Converter:
    def __init__(self, data=None):
        self._data = data
        self.datastring = {"raw": 0, type: "int"}
        self.datatype = None

    @staticmethod
    async def converter(self, data: dict):
        if data.get("type") == "str":
            return data.get("raw")
        elif data.get("type") == "int":
            return int(data.get("raw"))
        elif data.get("type") == "bytes":
            return bytes(data.get("raw"), encoding="utf-8")
        elif isinstance(data, list):
            return ast.literal_eval(data.get("raw"))
        elif isinstance(data, tuple):
            return ast.literal_eval(data.get("raw"))
        elif isinstance(data, float):
            return ast.literal_eval(data.get("raw"))
        elif isinstance(data, bool):
            return ast.literal_eval(data.get("raw"))
        elif isinstance(data, dict):
            return ast.literal_eval(data.get("raw"))
        else:
            output = await compile(fn_name="funfetch_compiler", code=data.get("raw"))
            if output.error:
                raise CompileError(
                    f"FunFetch Code Compile Error\nError Type: {output.error_type}\nTraceBack:\n{output.error_msg}"
                )
            else:
                return output.result

    @staticmethod
    async def compile(self, fn_name: str, code: str):
        cmd = code.strip()
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        body = f"async def {fn_name}(compiler):\n{cmd}"

        error = None

        try:
            parsed = ast.parse(body)
        except Exception:
            error = ("Parsing Error", traceback.format_exc())
            source = code

        if not error:
            body = parsed.body[0].body
            insert_returns(body)
            source = astunparse.unparse(parsed)

            env = {"compiler": compile}
            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            try:
                func = eval(fn_name, env)
                result = await func()
            except Exception:
                error = ("Executing Error", traceback.format_exc())
        if error:
            return CompileOutput(
                source=source, error=True, error_type=error[0], error_msg=error[1]
            )
        return CompileOutput(source=source, error=False, result=result)

    @classmethod
    async def return_dict(cls, jsondata: dict):
        return_dict_data = {}
        for x, y in dict.keys(), dict.values():
            data = await cls.converter(y)
            return_dict_data[x] = data
        return return_dict_data

    async def check(self):
        if isinstance(self._data, str):
            self.datatype = str
            self.datastring = {"raw": str(self._data), type: "str"}
        elif isinstance(self._data, int):
            self.datatype = int
            self.datastring = {"raw": str(self._data), type: "int"}
        elif isinstance(self._data, bytes):
            self.datatype = bytes
            self.datastring = {"raw": str(self._data.decode("utf-8")), type: "bytes"}
        elif isinstance(self._data, list):
            self.datatype = list
            self.datastring = {"raw": str(self._data), type: "list"}
        elif isinstance(self._data, tuple):
            self.datatype = tuple
            self.datastring = {"raw": str(list(self._data)), type: "tuple"}
        elif isinstance(self._data, float):
            self.datatype = float
            self.datastring = {"raw": str(self._data), type: "float"}
        elif isinstance(self._data, bool):
            self.datatype = bool
            self.datastring = {"raw": str(self._data), type: "bool"}
        elif isinstance(self._data, dict):
            self.datatype = dict
            self.datastring = {"raw": str(self._data), type: "dict"}
        else:
            self.datatype = AnyType
            self.datastring = {"raw": str(self._data), type: "anytype"}
