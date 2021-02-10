News for wurfapi
=================

This file lists the major changes between versions. For a more detailed list
of every change, see the Git log.

Latest
------
* Major: Extend function_synopsis to support selectors that contain multiple
  functions.

7.2.0
-----
* Minor: Extend ``cppreference_mappings`` to also include ``size_t``.

7.1.3
-----
* Patch: Fix issue with punctuations ending up in the wrong location.

7.1.2
-----
* Patch: Changed how paragraphs are (re)constructed. This means there are no
  longer trailing spaces, and links can now be followed by punctuations.
* Patch: Fix `Member Function Description` -> `Member Function Descriptions`.

7.1.1
-----
* Patch: Fix issue with links to free functions without scopes.
  The label is now ``function()`` rather than ``None::functions()``.

7.1.0
-----
* Minor: Added the WurfapiTarget directive for generating labels with default
  captions. This allows function and other entities to be linked easily
  without the need for creating e.g. a section or manually adding the label
  caption (as described here: https://github.com/sphinx-doc/sphinx/issues/2025).

7.0.0
-----
* Minor: Added user data option for templates.
* Patch: Add fix to mitigate a doxygen bug which causes member functions
  that shares the name a type to be linked as the parameter type in other member
  functions.
* Major: Changed location info to contain only a line instead of line-start and
  line-end. Location should point to where something is declared. Later we
  may add a body-location which point to the definition. Previously we were
  mixing the body location and that meant line numbers came from different files
  and therefore were wrong.
* Minor: Added the 'define' element to the API.

6.0.1
-----
* Patch: Fix issue with context missing when using function_synopsis.

6.0.0
-----
* Major: Reworked the way paragraphs are handled.

5.1.1
-----
* Patch: Changed named argument for Sphinx.add_directive and added
  requirement for sphinx>3.

5.1.0
-----
* Minor: Add support for trailing return types.
* Minor: Added const specifier in member the class synopsis template.

5.0.0
-----
* Minor: Add support file file links.
* Major: Drop Python 2.X support.

4.0.0
-----
* Major: Added a parameter type and better support for function parameters (
  we were missing arrays and default arguments).
* Major: Remove the `signature` item since it is not really used anywhere.
* Minor: Output the rst generated for the different directives in the `tmp`
  folder for debugging.
* Major: Remove testing of Python 3.4. since it has been deprecated.

3.0.0
-----
* Major: Change api_sort jinja2 helper to support accessing nested items in
  api dictionary.
* Minor: Change the default sort of members to match where they are declared
  in the hpp file.
* Major: Update location information to contain both path within project, and
  an optional include path.
* Minor: Enabeling support of user templates.
* Minor: Add link to bool type
* Major: Adding inline namespace support.
* Major: Add template support
* Major: Made function return values optional - such that constructors and
  destructors will not have that key.
* Patch: Fix extra white space when printing constructor and destructors.
* Major: Make value attributes optional
* Major: Make name of parameters optional
* Major: Enforce scope as either a string or None
* Major: Make link attribute optional.
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

