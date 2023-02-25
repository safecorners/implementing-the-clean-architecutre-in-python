# Implementing the Clean Architecutre In Python

## Business Requirements

- Bidder can place bids on auctions to win them
- An auction has a current price that is visible for all bidders
  - current price is determined by the amount of the lowest winning bid
  - to become a winner, one has to offer a price higher than the current price
- Action has a starting price. new bids with an amount lower than the starting price must not be accepted
