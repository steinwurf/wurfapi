.. _project::coffee::mug_size:

enum mug_size
=============

**Scope:** project::coffee

**In header:** ``#include <coffee/mug_size.h>``

Brief Description
-----------------

Different size coffee mugs. 

Values
------

.. list-table::
   :header-rows: 1
   :widths: auto

   * - Constant
     - Value
     - Description
   * - ``mug_size::Short``
     - 8
     - The Short version. 
   * - ``mug_size::Tall``
     - 
     - The Tall version. 
   * - ``mug_size::Grande``
     - 
     - The Grande version Use it like so: ``std::cout << mug_size::Grande << std::endl;`` 
   * - ``mug_size::Venti``
     - 20
     - The Venti version 20 ounces. This one will keep you up all night! 
       .. code-block:: c++

           std::cout << mug_size::Venti << std::endl;


       I hope you enjoy. 

Detailed Description
---------------------

This lets you choose the size of your coffee mug 
