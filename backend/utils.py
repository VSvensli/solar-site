# from pathlib import Path
# from dataclasses import dataclass


# @dataclass
# class TypeScriptType:
#     name: str
#     parameters: list[str]
#     dtypes: list[str]


# def extract_type_name(code: str) -> str:
#     keyword = "export type"
#     start = code.find(keyword)
#     if start == -1:
#         raise ValueError("Keyword 'export type' not found.")

#     start += len(keyword)
#     remaining = code[start:].strip()

#     eq_index = remaining.find("=")
#     if eq_index == -1:
#         raise ValueError("Equal sign '=' not found after the type name.")

#     type_name = remaining[:eq_index].strip()
#     return type_name


# def extract_parameters(code):
#     start = code.find("{")
#     end = code.rfind("}")
#     if start == -1 or end == -1:
#         print("Invalid TypeScript type definition.")

#     content = code[start + 1 : end].strip()
#     lines = content.split(";")

#     names = []
#     dtypes = []
#     for line in lines:
#         line = line.strip()
#         if not line:
#             continue
#         if ":" in line:
#             name, data_type = line.split(":", 1)
#             name = name.strip()
#             data_type = data_type.strip()
#             names.append(name)
#             dtypes.append(data_type)

#     return names, dtypes


# def parse_types_file(file_path: Path):
#     with open(file_path, "r") as f:
#         lines = f.readlines()

#     type_head_tail = [
#         i for i, line in enumerate(lines) if "export type" in line or "}" in line
#     ]
#     pairs = list(zip(type_head_tail[::2], type_head_tail[1::2], strict=True))
#     ts_types = ["".join(lines[head : tail + 1]) for head, tail in pairs]

#     typestript_types = []
#     for ts_code in ts_types:
#         name = extract_type_name(ts_code)
#         parameter_names, dtypes = extract_parameters(ts_code)
#         typestript_types.append(
#             TypeScriptType(name=name, parameters=parameter_names, dtypes=dtypes)
#         )
#     return typestript_types


# if __name__ == "__main__":
#     a = parse_types_file("src/stores/user.types.ts")
#     print(a)
