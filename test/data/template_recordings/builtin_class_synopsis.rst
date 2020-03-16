

.. _project::v1_0_0::coffee::machine:

class machine
=============

**Scope:** project::v1_0_0::coffee

**In header:** ``#include <coffee/coffee.h>``

Brief description
-----------------
A machine to brew your coffee. Docs by `http://steinwurf.com <http://steinwurf.com>`_\  . 


Member types (public)
---------------------

.. list-table::
   :header-rows: 0
   :widths: auto
   :align: left

   * - using
     - :ref:`callback<project::v1_0_0::coffee::machine::callback>` 
   * - typedef
     - :ref:`other_callback<project::v1_0_0::coffee::machine::other_callback>` 
   * - enum
     - :ref:`power<project::v1_0_0::coffee::machine::power>` { on, off }
   * - struct
     - :ref:`water_tank<project::v1_0_0::coffee::machine::water_tank>` 



Member functions (public)
-------------------------

.. list-table::
   :header-rows: 0
   :widths: auto
   :align: left

   * - 
     - :ref:`machine<project::v1_0_0::coffee::machine::machine()>` ()
   * - 
     - :ref:`machine<project::v1_0_0::coffee::machine::machine(powerpwr)>` (:ref:`power <project::v1_0_0::coffee::machine::power>`\  pwr)
   * - 
     - :ref:`~machine<project::v1_0_0::coffee::machine::~machine()>` ()
   * - void
     - :ref:`set_power<project::v1_0_0::coffee::machine::set_power(power)>` (:ref:`power <project::v1_0_0::coffee::machine::power>`\ )
   * - void
     - :ref:`set_number_cups<project::v1_0_0::coffee::machine::set_number_cups(uint32_tcups=0)>` (uint32_t cups = 0)
   * - void
     - :ref:`set_number_cups<project::v1_0_0::coffee::machine::set_number_cups(std::stringcups)>` (std::string cups)
   * - virtual uint32_t
     - :ref:`number_cups<project::v1_0_0::coffee::machine::number_cups()const>` () const
   * - const :ref:`water_tank <project::v1_0_0::coffee::machine::water_tank>`\  &
     - :ref:`tank<project::v1_0_0::coffee::machine::tank()const>` () const
   * - :ref:`water_tank <project::v1_0_0::coffee::machine::water_tank>`\  &
     - :ref:`tank<project::v1_0_0::coffee::machine::tank()>` ()
   * - std::vector< :ref:`water_tank <project::v1_0_0::coffee::machine::water_tank>`\  >
     - :ref:`tanks<project::v1_0_0::coffee::machine::tanks()>` ()
   * - void
     - :ref:`add_beans<project::v1_0_0::coffee::machine::add_beans<class,uint32_t>(constBeans&beans)>` (const Beans & beans)
   * - uint32_t
     - :ref:`get_bean_count<project::v1_0_0::coffee::machine::get_bean_count(mug_sizesize_of_mug)const>` (mug_size size_of_mug) const
   * - auto
     - :ref:`get_last_cup<project::v1_0_0::coffee::machine::get_last_cup()const>` () const
   * - mug_size
     - :ref:`get_mug_size<project::v1_0_0::coffee::machine::get_mug_size()const>` () const
   * - void
     - :ref:`set_name<project::v1_0_0::coffee::machine::set_name(constcharname[40])>` (const char name[40])




Static member functions (public)
--------------------------------

.. list-table::
   :header-rows: 0
   :widths: auto
   :align: left

   * - std::string
     - :ref:`version<project::v1_0_0::coffee::machine::version()>` ()



Member variables (public)
-------------------------

.. list-table::
   :header-rows: 1
   :widths: auto
   :align: left

   * - Type
     - Name
     - Value
     - Description
   * - uint32_t
     - cups_brewed
     - 0
     - The number of cups brewed by this machine. 
   * - :ref:`callback <project::v1_0_0::coffee::machine::callback>`\ 
     - m_callback
     - 
     - A variable which uses the callback using statement. 
   * - :ref:`other_callback <project::v1_0_0::coffee::machine::other_callback>`\ 
     - m_other_callback
     - 
     - A variable which uses the other_callback typedef statement. 




Static member variables (public)
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: auto
   :align: left

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
The coffee machine object serves as your applications entry point for brewing coffee. You have to remember to fill the project::coffee::machine::water_tank though. 




Member Function Description
---------------------------

.. _project::v1_0_0::coffee::machine::machine():

| **machine** ()

    Constructor. 


-----

.. _project::v1_0_0::coffee::machine::machine(powerpwr):

| **machine** (:ref:`power <project::v1_0_0::coffee::machine::power>`\  pwr)

    Constructor with power. 


-----

.. _project::v1_0_0::coffee::machine::~machine():

| **~machine** ()

    Destructor. 


-----

.. _project::v1_0_0::coffee::machine::set_power(power):

| void **set_power** (:ref:`power <project::v1_0_0::coffee::machine::power>`\ )

    Set the power of the machine. 


-----

.. _project::v1_0_0::coffee::machine::set_number_cups(uint32_tcups=0):

| void **set_number_cups** (uint32_t cups = 0)

    Set the number of cups to brew. 

    Before setting number of cups, check the following: 

    #. You have enough water in the :ref:`water_tank <project::v1_0_0::coffee::machine::water_tank>`\  . 

       - Of course you also need power. 

         .. code-block:: c++

             std::cout << "You need power" << std::endl;
             std::cout << "So plug it in" << std::endl;






       - A stable surface is also important! 





    #. Your coffee mug is clean. 

    You can see :ref:`number_cups() <project::v1_0_0::coffee::machine::number_cups()const>`\  for how many cups 

    Parameter ``cups``:
        The number of cups 





-----

.. _project::v1_0_0::coffee::machine::set_number_cups(std::stringcups):

| void **set_number_cups** (std::string cups)

    Set the number of cups to brew. 

    Before setting number of cups, check the following: 

    #. You have enough water in the :ref:`water_tank <project::v1_0_0::coffee::machine::water_tank>`\  . 

       - Of course you also need power. 

         .. code-block:: c++

             std::cout << "You need power" << std::endl;
             std::cout << "So plug it in" << std::endl;






       - A stable surface is also important! 





    #. Your coffee mug is clean. 

    You can see :ref:`number_cups() <project::v1_0_0::coffee::machine::number_cups()const>`\  for how many cups 

    Parameter ``cups``:
        The number of cups 





-----

.. _project::v1_0_0::coffee::machine::number_cups()const:

| uint32_t **number_cups** () const

    Returns:
        The number of cups 


-----

.. _project::v1_0_0::coffee::machine::version():

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




-----

.. _project::v1_0_0::coffee::machine::tank()const:

| const :ref:`water_tank <project::v1_0_0::coffee::machine::water_tank>`\  & **tank** () const

    Get the first water tank. 


-----

.. _project::v1_0_0::coffee::machine::tank():

| :ref:`water_tank <project::v1_0_0::coffee::machine::water_tank>`\  & **tank** ()

    Get the first water tank. 


-----

.. _project::v1_0_0::coffee::machine::tanks():

| std::vector< :ref:`water_tank <project::v1_0_0::coffee::machine::water_tank>`\  > **tanks** ()

    Get all water tanks. 


-----

.. _project::v1_0_0::coffee::machine::add_beans<class,uint32_t>(constBeans&beans):

| template <class Beans = Arabica, uint32_t BeanSize = 100>
| void **add_beans** (const Beans & beans)

    Add a generic beans 

    Template parameter: class ``Beans``  = Arabica
        The generic bean type 

    Template parameter: uint32_t ``BeanSize``  = 100
        The size of a bean 



-----

.. _project::v1_0_0::coffee::machine::get_bean_count(mug_sizesize_of_mug)const:

| auto **get_bean_count** (mug_size size_of_mug) const -> uint32_t

    Get the number of beans needed for a given mug. 


-----

.. _project::v1_0_0::coffee::machine::get_last_cup()const:

| auto **get_last_cup** () const

    Get the last cup of coffee. 


-----

.. _project::v1_0_0::coffee::machine::get_mug_size()const:

| mug_size **get_mug_size** () const

    This header is `src/coffee/coffee.h` if this is important? Also there is an example in `examples/header/header.h` 

    Returns:
        the mug_size 


-----

.. _project::v1_0_0::coffee::machine::set_name(constcharname[40]):

| void **set_name** (const char name[40])

    Set the machine name. 










Type Description
----------------

.. _project::v1_0_0::coffee::machine::callback:

using **callback** = std::function< void()>

    The generic callback type. 

    

-----

.. _project::v1_0_0::coffee::machine::other_callback:

typedef :ref:`callback <project::v1_0_0::coffee::machine::callback>`\  **other_callback**

    Another way to define a type is a typedef. 

    









