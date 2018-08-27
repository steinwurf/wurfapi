







.. _project::coffee::machine:

class machine
=============


**Scope:** project::coffee


**In header:** ``#include <coffee/coffee.h>``


Brief description
-----------------
A machine to brew your coffee. 



Member functions (public)
-------------------------

.. list-table::
   :header-rows: 0
   :widths: auto



   * - virtual uint32_t
     - :ref:`number_cups<project::coffee::machine::number_cups()const>` () const


   * - void
     - :ref:`set_number_cups<project::coffee::machine::set_number_cups(std::string)>` (std::string cups)


   * - void
     - :ref:`set_number_cups<project::coffee::machine::set_number_cups(uint32_t)>` (uint32_t cups)


   * - water_tank
     - :ref:`tank<project::coffee::machine::tank()>` ()







Static member functions (public)
--------------------------------

.. list-table::
   :header-rows: 0
   :widths: auto



   * - std::string
     - :ref:`version<project::coffee::machine::version()>` ()



Description
-----------
The coffee machine object serves as your applications entry point for brewing coffee. You have to remember to fill the :ref:`project::coffee::machine::water_tank<project::coffee::machine::water_tank>` though. 







Member Function Description
---------------------------

.. _project::coffee::machine::number_cups()const:

uint32_t **number_cups** ()

    

    

    

    Returns:
        The number of cups 



-----

.. _project::coffee::machine::set_number_cups(std::string):

void **set_number_cups** (std::string cups)

    Set the number of cups to brew. 

    Before setting number of cups, check the following: 

    #. You have enough water in the :ref:`water_tank<project::coffee::machine::water_tank>` . 

       - Of course you also need power. 

         .. code-block:: c++

             std::cout << "You need power" << std::endl;
             std::cout << "So plug it in" << std::endl;



       - A stable surface is also important! 
    #. Your coffee mug is clean. You can see :ref:`number_cups()<project::coffee::machine::number_cups()const>` for how many cups 

    
    Parameter ``cups``:
        The number of cups 


    



-----

.. _project::coffee::machine::set_number_cups(uint32_t):

void **set_number_cups** (uint32_t cups)

    Set the number of cups to brew. 

    Before setting number of cups, check the following: 

    #. You have enough water in the :ref:`water_tank<project::coffee::machine::water_tank>` . 

       - Of course you also need power. 

         .. code-block:: c++

             std::cout << "You need power" << std::endl;
             std::cout << "So plug it in" << std::endl;



       - A stable surface is also important! 
    #. Your coffee mug is clean. You can see :ref:`number_cups()<project::coffee::machine::number_cups()const>` for how many cups 

    
    Parameter ``cups``:
        The number of cups 


    



-----

.. _project::coffee::machine::tank():

water_tank **tank** ()

    Get the water tank. 

    

    

    



-----

.. _project::coffee::machine::version():

std::string **version** ()

    The version of the machine. 

    Example: 

    .. code-block:: c++

        std::cout << "The version";
                   << project::coffee::machine::version() << "\n";


    Remember to use ``\n`` rather than ``std::endl`` it is more efficient. 

    

    Returns:
        The version of the machine. Example: 

        .. code-block:: c++

            std::cout << machine::version();
            std::cout << "\n";












