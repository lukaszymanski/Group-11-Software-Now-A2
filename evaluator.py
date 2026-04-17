import os

INPUT_FILE = "expressions.txt"
OUTPUT_FILE = "output.txt"


def tokenize(expr):
    tokens = []
    i = 0

    while i < len(expr):
        ch = expr[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit():
            num = ch
            i += 1
            while i < len(expr) and expr[i].isdigit():
                num += expr[i]
                i += 1
            tokens.append(("NUM", int(num)))
            continue

        if ch in "+-*/":
            tokens.append(("OP", ch))
            i += 1
            continue

        if ch == "(":
            tokens.append(("LPAREN", ch))
            i += 1
            continue

        if ch == ")":
            tokens.append(("RPAREN", ch))
            i += 1
            continue

        return "ERROR"

    tokens.append(("END", None))
    return tokens


def format_tokens(tokens):
    if tokens == "ERROR":
        return "ERROR"

    parts = []
    for token_type, value in tokens:
        if token_type == "NUM":
            parts.append(f"[NUM:{value}]")
        elif token_type == "OP":
            parts.append(f"[OP:{value}]")
        elif token_type == "LPAREN":
            parts.append(f"[LPAREN:{value}]")
        elif token_type == "RPAREN":
            parts.append(f"[RPAREN:{value}]")
        elif token_type == "END":
            parts.append("[END]")

    return " ".join(parts)


def current_token(tokens, pos):
    return tokens[pos]


def eat_token(pos):
    return pos + 1


def parse_expression(tokens, pos):
    node, pos = parse_term(tokens, pos)

    while current_token(tokens, pos)[0] == "OP" and current_token(tokens, pos)[1] in ("+", "-"):
        op = current_token(tokens, pos)[1]
        pos = eat_token(pos)
        right, pos = parse_term(tokens, pos)
        node = (op, node, right)

    return node, pos


def parse_term(tokens, pos):
    node, pos = parse_unary(tokens, pos)

    while True:
        current = current_token(tokens, pos)

        if current[0] == "OP" and current[1] in ("*", "/"):
            op = current[1]
            pos = eat_token(pos)
            right, pos = parse_unary(tokens, pos)
            node = (op, node, right)

        elif current[0] in ("NUM", "LPAREN"):
            right, pos = parse_unary(tokens, pos)
            node = ("*", node, right)

        else:
            break

    return node, pos


def parse_unary(tokens, pos):
    current = current_token(tokens, pos)

    if current[0] == "OP" and current[1] == "-":
        pos = eat_token(pos)
        operand, pos = parse_unary(tokens, pos)
        return ("neg", operand), pos

    if current[0] == "OP" and current[1] == "+":
        raise ValueError("Unary plus is not supported")

    return parse_primary(tokens, pos)


def parse_primary(tokens, pos):
    current = current_token(tokens, pos)

    if current[0] == "NUM":
        return current[1], eat_token(pos)

    if current[0] == "LPAREN":
        pos = eat_token(pos)
        node, pos = parse_expression(tokens, pos)

        if current_token(tokens, pos)[0] != "RPAREN":
            raise ValueError("Missing closing parenthesis")

        pos = eat_token(pos)
        return node, pos

    raise ValueError("Invalid expression")


def parse(tokens):
    node, pos = parse_expression(tokens, 0)

    if current_token(tokens, pos)[0] != "END":
        raise ValueError("Extra input")

    return node


def tree_to_string(node):
    if isinstance(node, int):
        return str(node)

    if node[0] == "neg":
        return f"(neg {tree_to_string(node[1])})"

    op, left, right = node
    return f"({op} {tree_to_string(left)} {tree_to_string(right)})"


def evaluate_tree(node):
    if isinstance(node, int):
        return node

    if node[0] == "neg":
        return -evaluate_tree(node[1])

    op, left, right = node
    left_val = evaluate_tree(left)
    right_val = evaluate_tree(right)

    if op == "+":
        return left_val + right_val

    if op == "-":
        return left_val - right_val

    if op == "*":
        return left_val * right_val

    if op == "/":
        if right_val == 0:
            raise ZeroDivisionError("Division by zero")
        return left_val / right_val

    raise ValueError("Unknown operator")


def format_result(value):
    if value == "ERROR":
        return "ERROR"

    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return f"{value:.4f}"

    return str(value)


def write_output_file(results, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for item in results:
            f.write(f"Input: {item['input']}\n")
            f.write(f"Tree: {item['tree']}\n")
            f.write(f"Tokens: {item['tokens']}\n")
            f.write(f"Result: {item['result']}\n\n")


def evaluate_file(input_path: str) -> list[dict]:
    results = []

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        expr = line.rstrip("\n")

        if expr.strip() == "":
            continue

        tokens = tokenize(expr)

        if tokens == "ERROR":
            results.append({
                "input": expr,
                "tree": "ERROR",
                "tokens": "ERROR",
                "result": "ERROR"
            })
            continue

        try:
            tree = parse(tokens)
            value = evaluate_tree(tree)
            result_str = format_result(value)

            results.append({
                "input": expr,
                "tree": tree_to_string(tree),
                "tokens": format_tokens(tokens),
                "result": result_str
            })

        except Exception:
            results.append({
                "input": expr,
                "tree": "ERROR",
                "tokens": "ERROR",
                "result": "ERROR"
            })

    output_path = os.path.join(os.path.dirname(input_path), OUTPUT_FILE)
    write_output_file(results, output_path)

    return results


def main():
    results = evaluate_file(INPUT_FILE)
    print(f"Processed {len(results)} expression(s). Output written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()