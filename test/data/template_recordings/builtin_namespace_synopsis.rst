






.. _project:

namespace project
=================





.. list-table::
   :header-rows: 0
   :widths: auto



   * - namespace
     - :ref:`coffee<project::coffee>`


   * - function
     - :ref:`print<project::print(double,int)>`


   * - function
     - :ref:`print<project::print(int,bool)>`










Functions
---------

.. _project::print(double,int):

void **print** (double a, int b)

    Prints the ``a`` and then the ``b`` . 

    This is really handy in case you need to see them. Example: 

    .. code-block:: c++

        std::cout << project::coffee::print(2.0, 1) << "\n";


    Remember to use ``\n`` rather than ``std::endl`` it is more efficient. 

    
    Parameter ``a``:
        A is actually a double. 

    Parameter ``b``:
        Whereas b is an int. 


    Returns:
        This does not really return anything because it is ``void`` but it could! 



-----

.. _project::print(int,bool):

void **print** (int a_number, bool on_paper)

    

    

    
    Parameter ``a_number``:
        This is the most important parameter. Without it the function will not work. Example: 

        .. code-block:: c++

            project::coffee::print(3);


        Does this work 

    Parameter ``on_paper``:
        If ``true`` print on some actual paper. 


    








