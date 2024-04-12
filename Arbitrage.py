liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

# 計算輸出量的函式
def calculate_amount_out(amount_in, reserve_in, reserve_out):
    assert amount_in > 0, 'UniswapV2Library: INSUFFICIENT_INPUT_AMOUNT'
    assert reserve_in > 0 and reserve_out > 0, 'UniswapV2Library: INSUFFICIENT_LIQUIDITY'
    fee_adjusted_amount_in = amount_in * 997
    numerator = fee_adjusted_amount_in * reserve_out
    denominator = reserve_in * 1000 + fee_adjusted_amount_in
    return numerator / denominator

# 根據代幣進行換算的函式
def swap_tokens(token_in, token_out, amount_in):
    pair_key = (token_in, token_out) if (token_in, token_out) in liquidity else (token_out, token_in)
    reserves = liquidity[pair_key]
    reserve_in, reserve_out = reserves if pair_key == (token_in, token_out) else (reserves[1], reserves[0])
    return calculate_amount_out(amount_in, reserve_in, reserve_out)

# 計算代幣路徑交換後的餘額
def calculate_token_path(path, initial_amount):
    amount = initial_amount
    for i in range(len(path) - 1):
        amount = swap_tokens(path[i], path[i+1], amount)
    return amount

# 格式化輸出路徑和餘額的函式
def display_results(token_path, final_amount):
    path_str = "->".join(token_path)
    balance_str = f"{final_amount:.6f}"  # 保留六位小數
    print(f"path: {path_str}, tokenB balance={balance_str}")

# 產生不同的路徑並計算結果
def explore_paths(token_set):
    def explore(path, remaining_tokens):
        if path and path not in seen:
            token_sequence = ["tokenB"] + [f"token{ch}" for ch in path] + ["tokenB"]
            result = calculate_token_path(token_sequence, 5)
            if result >= 20:
                display_results(token_sequence, result)
            seen.add(path)
        
        for i in range(len(remaining_tokens)):
            explore(path + remaining_tokens[i], remaining_tokens[:i] + remaining_tokens[i+1:])

    seen = set()
    explore("", token_set)

explore_paths("ACDE")
