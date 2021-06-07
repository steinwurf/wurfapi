Examples
========

These are some examples you can use to get started with your
own application.

.. contents::
    :local:

Basic Example
.............

We should also be able to generate links to the member functions using ``ref``
and the unique name of the entity.

Let's see if it works:

:wurfapi:`project::coffee::machine::set_number_cups`

:wurfapi:`project::coffee::machine::set_number_hops`

:wurfapi:`project::coffee::machine::set_number_cups(std::string`

:ref:`project::coffee::machine::set_number_cups(std::stringcups)`


.. literalinclude:: ../examples/basic_coffee/basic_coffee.cpp
    :language: c++

Advanced Example
................

.. literalinclude:: ../examples/advanced_coffee/advanced_coffee.cpp
    :language: c++