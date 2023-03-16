# [Implementing the Clean Architecutre In Python](https://github.com/Enforcer/clean-architecture)

## Business Requirements

- Bidder can place bids on auctions to win them
- An auction has a current price that is visible for all bidders
  - current price is determined by the amount of the lowest winning bid
  - to become a winner, one has to offer a price higher than the current price
- Action has a starting price. new bids with an amount lower than the starting price must not be accepted

## Testing

### The Layers of Testing

1. Business Logic (Entity) Should be Unit Tested in a black-box way
2. Application Business Rules (UseCases) fall under Service Testing
3. Repositories and Adapters will benefit most from the integration testing
4. API Test
5. User Interface Test
6. Acceptance Test
7. Web Framework Test
8. e2e Test

### Unit-Testing of An Entire Module

1. Putting a system under test in the the desired state (Arrange / Given)
2. Invoking an action of the system under test (Act / When)
3. Verifying output of action from point 2. (Assert / Then) assert bout:
   - Output DTO, if we use Output Boundary + Presenter
   - Exceptions Thrown
   - which **Domain Events** have been emitted from within the module
   - how mocks for *Ports* are used
4. Dealing with dependencies (Ports & Repositories) using Test Doubles

### General Testing Strategy

- heavy unit-tests for the entire module, with faked Repositories and mocked Ports
- no unit tests for individual classes inside the Clean Architecture modules, unless they are things like calculators or validators and it is very impractical to test them with the entire module
- higher-level tests for Facade-based modules, without test doubles for database
- alway have tests to check external providers, at minimum mimic the real usage of it, e.g. charge payment card, then capture
- at least three API-level tests for each Use Case / Facade method to check positive scenario, negative scenario and to check if authorization is working
- a couple of UI tests will cover several endpoints at once
- do not do automated acceptance testing on the level of UI

## References

- [Deep Dive into PIP - 1](https://suhwan.dev/2018/10/24/deep-dive-into-pip-1/)
- [Deep Dive into PIP - 2](https://suhwan.dev/2018/10/30/deep-dive-into-pip-2/)
