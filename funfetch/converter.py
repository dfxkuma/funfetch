import ast
import astunparse
import traceback
from .model import AnyType, CompileOutput
from .errors import CompileError
from .utils import insert_returns


class Converter:
    @staticmethod
    async def converter(data: dict):
        if data.get("type") == "str":
            return data.get("raw")
        elif data.get("type") == "int":
            return int(data.get("raw"))
        elif data.get("type") == "bytes":
            return bytes(data.get("raw"), encoding="utf-8")
        elif data.get("type") == "list":
            return ast.literal_eval(data.get("raw"))
        elif data.get("type") == "tuple":
            return ast.literal_eval(data.get("raw"))
        elif data.get("type") == "float":
            return ast.literal_eval(data.get("raw"))
        elif data.get("type") == "bool":
            return ast.literal_eval(data.get("raw"))
        elif data.get("type") == "dict":
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
        for x, y in zip(jsondata.keys(), jsondata.values()):
            data = await cls.converter(data=jsondata[x])
            return_dict_data[x] = data
        return return_dict_data

    @classmethod
    async def converter_string(cls, jsondata: dict):
        return_dict_data = {}
        for x, y in zip(jsondata.keys(), jsondata.values()):
            data = await cls.check(obj=y)
            return_dict_data[x] = data
        return return_dict_data

    @classmethod
    async def check(cls, obj):
        if isinstance(obj, str):
            datatype = str
            datastring = {"raw": str(obj), "type": "str"}
            return datastring
        elif isinstance(obj, int):
            datatype = int
            datastring = {"raw": str(obj), "type": "int"}
            return datastring
        elif isinstance(obj, bytes):
            datatype = bytes
            datastring = {"raw": str(obj.decode("utf-8")), "type": "bytes"}
            return datastring
        elif isinstance(obj, list):
            datatype = list
            datastring = {"raw": str(obj), "type": "list"}
            return datastring
        elif isinstance(obj, tuple):
            datatype = tuple
            datastring = {"raw": str(list(obj)), "type": "tuple"}
            return datastring
        elif isinstance(obj, float):
            datatype = float
            datastring = {"raw": str(obj), "type": "float"}
            return datastring
        elif isinstance(obj, bool):
            datatype = bool
            datastring = {"raw": str(obj), "type": "bool"}
            return datastring
        elif isinstance(obj, dict):
            datatype = dict
            datastring = {"raw": str(obj), "type": "dict"}
            return datastring
        else:
            datatype = AnyType
            datastring = {"raw": str(obj), "type": "anytype"}
            return datastring
