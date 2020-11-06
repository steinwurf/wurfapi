function print(double a, int \* b)
----------------------------------

**Scope:** project::v1_0_0

**In header:** ``#include <coffee/coffee.h>``

.. wurfapitarget:: project::v1_0_0::print(doublea,int*b)
    :label: project::v1_0_0::print()

| void **print** (double a, int \* b)

    Prints the ``a`` and then the value pointed to by ``b``.



    This is really handy in case you need to see them.

    Example: 

    .. code-block:: c++

        std::cout << project::coffee::print(2.0, &value) << "\n";




    Remember to use ``\n`` rather than ``std::endl`` it is more efficient.



    Parameter ``a``:
        A is actually a double.




    Parameter ``b``:
        Whereas b is a pointer to an int.






    Returns:
        This does not really return anything because it is ``void`` but it could!


