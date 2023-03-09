# Money Value Object

`Money` Type should have:

- it should be immutable - once created, cannot be changed
- it must not be possible to create such an object with an invaild state. Decimal('python') raises an exception
- it represents value, not a long-living object - it has no identity
- instances with the same value are always considered equal

`Money` specific:

- it should support arithmetic operations, just like `Decimal` does
