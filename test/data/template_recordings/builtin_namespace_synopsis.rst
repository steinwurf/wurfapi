
.. _project::v1_0_0:

namespace v1_0_0
================

**Scope:** project


.. list-table::
   :header-rows: 0
   :widths: auto
   :align: left


   * - namespace
     - :ref:`coffee <project::v1_0_0::coffee>`\ 
   * - function
     - :ref:`print <project::v1_0_0::print(doublea,int*b)>`\ 
   * - function
     - :ref:`print <project::v1_0_0::print(inta_number,boolon_paper)>`\ 


Functions
---------

.. _project::v1_0_0::print(doublea,int*b):

| void **print** (double a, int \* b)

    Prints the ``a`` and then the value pointed to by ``b`` . 

    This is really handy in case you need to see them. Example: 

    .. code-block:: c++

        std::cout << project::coffee::print(2.0, &value) << "\n";


    Remember to use ``\n`` rather than ``std::endl`` it is more efficient. 

    Parameter ``a``:
        A is actually a double. 


    Parameter ``b``:
        Whereas b is a pointer to an int. 




    Returns:
        This does not really return anything because it is ``void`` but it could! 


-----

.. _project::v1_0_0::print(inta_number,boolon_paper):

| void **print** (int a_number, bool on_paper)

    Parameter ``a_number``:
        This is the most important parameter. Without it the function will not work. Example: 

        .. code-block:: c++

            project::coffee::print(3);


        Does this work 


    Parameter ``on_paper``:
        If ``true`` print on some actual paper. 







