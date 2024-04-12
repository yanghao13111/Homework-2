# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution

- Path: tokenB->tokenA->tokenD->tokenC->tokenB

- Swap from tokenB to tokenA: (amountIn, amountOut) = (5.00 ether, 5.655321988 ether)
- Swap from tokenA to tokenD: (amountIn, amountOut) = (5.655321988 ether, 2.458781317 ether)
- Swap from tokenD to tokenC: (amountIn, amountOut) = (2.458781317 ether, 5.088927293 ether)
- Swap from tokenC back to tokenB: (amountIn, amountOut) = (5.088927293 ether, 20.129888944 ether)
- Final tokenB balance: 20.129889 ether

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution

- Slippage in automated market makers (AMM) like Uniswap V2 refers to the difference between the expected price of a trade and the executed price. This variation is typically caused by price movements due to supply and demand changes when the trade is executed.

- Uniswap V2 mitigates slippage risks by allowing users to specify a minimum amount of tokens they are willing to accept in return, ensuring users do not experience losses greater than expected due to significant price changes during transaction execution.

```
router.swapExactTokensForTokens(
  5 ether,  // amount of tokens supplied
  20 ether, // minimum amount of tokens expected to receive
  path,     // trading path
  arbitrager, // recipient address
  block.timestamp + 300 // transaction deadline
);
```

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution

In the UniswapV2Pair contract, the mint function is utilized to add liquidity. When totalSupply is zero, indicating the first time liquidity is being added, Uniswap V2 subtracts a specific minimum liquidity amount denoted as MINIMUM_LIQUIDITY. The rationale includes:

1. Preventing pools from being drained to zero: By permanently locking away a small amount of liquidity, Uniswap ensures the pool can never be completely depleted through trades, which is especially critical at the initial stages of the pool.
2. Avoiding division by zero errors: In the AMM formula, the relative value of liquidity tokens is calculated based on the ratio of assets in the pool, which involves division by the pool's total supply.
3. Signifying that the pool has been initialized: The locked MINIMUM_LIQUIDITY acts as a marker that the pool has been set up.
4. Security reasons: By locking a minimum liquidity permanently, it helps prevent certain types of manipulative behaviors or attacks.

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution

- When adding liquidity to an existing Uniswap V2 pool, the amount of liquidity tokens (LP tokens) issued is determined by a formula designed to keep the issuance fair and proportional to the depositor’s contribution relative to the pool's current size.

The formula used is:

```
liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);
```

- This formula ensures that each liquidity provider receives an amount of LP tokens proportional to their contribution, thus maintaining the fairness of ownership distribution within the pool. Additionally, it prevents the dilution of existing LP tokens' value by ensuring that newly added liquidity is proportionate to the existing pool size.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution
- A sandwich attack is a type of manipulation observed on AMM-based decentralized exchanges. It targets users executing token swaps and can result in the user receiving a worse exchange rate than expected under normal conditions.

The attack involves four steps:

1. Identification: The attacker spots a pending transaction intending to swap a large amount of one token for another.
2. Front-running: The attacker executes a transaction with a higher gas fee to get it processed before the user's transaction. They buy the same token the user intends to buy, driving up the price.
3. User's transaction: The user's transaction is processed at the increased price, resulting in less token received than initially anticipated.
4. Back-running: The attacker sells the token they bought earlier at the increased price, profiting from the price difference created by the user's transaction.
If targeted by a sandwich attack during a swap, one may experience:

- Worse exchange rates: Due to the artificially inflated token prices.
- Financial losses: As a direct consequence of receiving fewer tokens.
- Market impact: Such attacks can exacerbate market volatility and undermine trust in the fairness and efficiency of decentralized exchanges.
