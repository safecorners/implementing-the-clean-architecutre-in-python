# [Implementing the Clean Architecutre In Python](https://github.com/Enforcer/clean-architecture)

## Business Requirements

- Bidder can place bids on auctions to win them
- An auction has a current price that is visible for all bidders
  - current price is determined by the amount of the lowest winning bid
  - to become a winner, one has to offer a price higher than the current price
- Action has a starting price. new bids with an amount lower than the starting price must not be accepted

## References

- [Deep Dive into PIP - 1](https://suhwan.dev/2018/10/24/deep-dive-into-pip-1/)
- [Deep Dive into PIP - 2](https://suhwan.dev/2018/10/30/deep-dive-into-pip-2/)
