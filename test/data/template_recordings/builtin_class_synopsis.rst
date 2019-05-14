
.. _project::coffee::machine:

class machine
=============

**Scope:** project::coffee

**In header:** ``#include <coffee/coffee.h>``

Brief description
-----------------
A machine to brew your coffee. Docs by `http://steinwurf.com <http://steinwurf.com>`_ . 


Member types (public)
---------------------

.. list-table::
   :header-rows: 0
   :widths: auto

   * - using
     - :ref:`callback<project::coffee::machine::callback>` 
   * - typedef
     - :ref:`other_callback<project::coffee::machine::other_callback>` 
   * - enum
     - :ref:`power<project::coffee::machine::power>` { on, off }
   * - struct
     - :ref:`water_tank<project::coffee::machine::water_tank>` 



Member functions (public)
-------------------------

.. list-table::
   :header-rows: 0
   :widths: auto

   * - 
     - :ref:`machine<project::coffee::machine::machine()>` ()
   * - 
     - :ref:`machine<project::coffee::machine::machine(power)>` (:ref:`power <project::coffee::machine::power>` pwr)
   * - 
     - :ref:`~machine<project::coffee::machine::~machine()>` ()
   * - void
     - :ref:`add_beans<project::coffee::machine::add_beans<class,uint32_t>(constBeans&)>` (const Beans & beans)
   * - mug_size
     - :ref:`get_mug_size<project::coffee::machine::get_mug_size()const>` () const
   * - virtual uint32_t
     - :ref:`number_cups<project::coffee::machine::number_cups()const>` () const
   * - void
     - :ref:`set_number_cups<project::coffee::machine::set_number_cups(std::string)>` (std::string cups)
   * - void
     - :ref:`set_number_cups<project::coffee::machine::set_number_cups(uint32_t)>` (uint32_t cups)
   * - void
     - :ref:`set_power<project::coffee::machine::set_power(power)>` (:ref:`power <project::coffee::machine::power>` )
   * - :ref:`water_tank <project::coffee::machine::water_tank>` &
     - :ref:`tank<project::coffee::machine::tank()>` ()
   * - const :ref:`water_tank <project::coffee::machine::water_tank>` &
     - :ref:`tank<project::coffee::machine::tank()const>` () const
   * - std::vector< :ref:`water_tank <project::coffee::machine::water_tank>` >
     - :ref:`tanks<project::coffee::machine::tanks()>` ()




Static member functions (public)
--------------------------------

.. list-table::
   :header-rows: 0
   :widths: auto

   * - std::string
     - :ref:`version<project::coffee::machine::version()>` ()



Member variables (public)
-------------------------

.. list-table::
   :header-rows: 1
   :widths: auto

   * - Type
     - Name
     - Value
     - Description
   * - uint32_t
     - cups_brewed
     - 0
     - The number of cups brewed by this machine. 
   * - :ref:`callback <project::coffee::machine::callback>`
     - m_callback
     - 
     - A variable which uses the callback using statement. 
   * - :ref:`other_callback <project::coffee::machine::other_callback>`
     - m_other_callback
     - 
     - A variable which uses the other_callback typedef statement. 




Static member variables (public)
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: auto

   * - Type
     - Name
     - Value
     - Description
   * - uint32_t
     - total_cups_brewed
     - 
     - The number of cups brewed by all machines. 



Description
-----------
The coffee machine object serves as your applications entry point for brewing coffee. You have to remember to fill the :ref:`project::coffee::machine::water_tank <project::coffee::machine::water_tank>` though. 




Member Function Description
---------------------------

.. _project::coffee::machine::machine():

| **machine** ()

    Constructor. 


-----

.. _project::coffee::machine::machine(power):

| **machine** (:ref:`power <project::coffee::machine::power>` pwr)

    Constructor with power. 


-----

.. _project::coffee::machine::~machine():

| **~machine** ()

    Destructor. 


-----

.. _project::coffee::machine::add_beans<class,uint32_t>(constBeans&):

| template <class Beans = Arabica, uint32_t BeanSize = 100>
| void **add_beans** (const Beans & beans)

    Add a genearic beans 

    Template parameter: class ``Beans``  = Arabica
        The generic bean type 

    Template parameter: uint32_t ``BeanSize``  = 100
        The size of a bean 



-----

.. _project::coffee::machine::get_mug_size()const:

| mug_size **get_mug_size** ()

    Returns:
        the mug_size 


-----

.. _project::coffee::machine::number_cups()const:

| uint32_t **number_cups** ()

    Returns:
        The number of cups 


-----

.. _project::coffee::machine::set_number_cups(std::string):

| void **set_number_cups** (std::string cups)

    Set the number of cups to brew. 

    Before setting number of cups, check the following: 

    #. You have enough water in the :ref:`water_tank <project::coffee::machine::water_tank>` . 

       - Of course you also need power. 

         .. code-block:: c++

             std::cout << "You need power" << std::endl;
             std::cout << "So plug it in" << std::endl;






       - A stable surface is also important! 





    #. Your coffee mug is clean. 

    You can see :ref:`number_cups() <project::coffee::machine::number_cups()const>` for how many cups 

    Parameter ``cups``:
        The number of cups 





-----

.. _project::coffee::machine::set_number_cups(uint32_t):

| void **set_number_cups** (uint32_t cups)

    Set the number of cups to brew. 

    Before setting number of cups, check the following: 

    #. You have enough water in the :ref:`water_tank <project::coffee::machine::water_tank>` . 

       - Of course you also need power. 

         .. code-block:: c++

             std::cout << "You need power" << std::endl;
             std::cout << "So plug it in" << std::endl;






       - A stable surface is also important! 





    #. Your coffee mug is clean. 

    You can see :ref:`number_cups() <project::coffee::machine::number_cups()const>` for how many cups 

    Parameter ``cups``:
        The number of cups 





-----

.. _project::coffee::machine::set_power(power):

| void **set_power** (:ref:`power <project::coffee::machine::power>` )

    Set the power of the machine. 


-----

.. _project::coffee::machine::tank():

| :ref:`water_tank <project::coffee::machine::water_tank>` & **tank** ()

    Get the first water tank. 


-----

.. _project::coffee::machine::tank()const:

| const :ref:`water_tank <project::coffee::machine::water_tank>` & **tank** ()

    Get the first water tank. 


-----

.. _project::coffee::machine::tanks():

| std::vector< :ref:`water_tank <project::coffee::machine::water_tank>` > **tanks** ()

    Get all water tanks. 


-----

.. _project::coffee::machine::version():

| std::string **version** ()

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












Type Description
----------------

.. _project::coffee::machine::callback:

using **callback** = std::function< void()>

    The generic callback type. 

    

-----

.. _project::coffee::machine::other_callback:

typedef :ref:`callback <project::coffee::machine::callback>` **other_callback**

    Another way to define a type is a typedef. 

    









