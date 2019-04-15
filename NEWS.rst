News for wurfapi
=================

This file lists the major changes between versions. For a more detailed list
of every change, see the Git log.

Latest
------
* Major: Added schema checking of parsed API json
* Major: Added link provider functionality and default mappings to cppreference.
* Major: Support both internal and external links.
* Patch: Fix variable constexpr / const parsing.
* Major: Split variables into static and non-static and only present the table.
* Major: Made type a list or items
* Minor: Improved link finding (more links to known types)
* Major: Made the type and location element uniform.
* Major: Changed certain elements' `type` key to kind.
* Minor: Support for variables
* Minor: Support for typedef and using in classes and structs
* Major: Allow multiple source paths to be specified.
* Minor: Adding support for lists (ordered and unordered).
* Patch: Fix parameter types in cases where Doxygen made them a link.
* Minor: Add sorting capabilities using the api_sort jinja2 filter.
* Major: Change api_filter function to be a jinja2 filter.
* Major: Changed way return value information is stored in the API dictionary.
* Minor: Add patch_api support for Doxygen. To allow manually patching Doxygen
  output if incorrect.
* Patch: Fix space in project name when constructing XML output path

2.2.0
-----
* Minor: Fix missing return_type when Doxygen put it in a nested
         ref tag

2.1.0
-----
* Minor: Fix broken 2.0.0 version number in wurfapi_directive.

2.0.0
-----
* Minor: Added support for enum
* Minor: Added warnings_as_error option to allow failure if Doxygen
         produces any warnings.
* Major: Significantly updated .rst templates
* Minor: Added api_filter helper function for running queries
         against the API.
* Major: Rewrote the Doxygen XML parser.

1.0.0
-----
* Initial release (still beta quality).

