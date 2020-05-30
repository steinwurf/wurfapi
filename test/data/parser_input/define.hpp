/**
 * @brief The version as a string
 *
 * Some more detailed description of when to use this define.
 */
#define VERSION "1.0.0"
#define TEST 0
#define NOVALUE

// Detect compilers and CPU architectures - none of these will be picked up
// by doxygen. Since we need to pass some Doxygen arguments to make that happen
#if defined(__clang__) || defined(__llvm__)
#if defined(__i386__) || defined(__x86_64__)
#define PLATFORM_X86 1
#endif
#elif defined(__GNUC__)
#if defined(__i386__) || defined(__x86_64__)
#define PLATFORM_X86 1
#endif
#elif defined(_MSC_VER)
#if defined(_M_IX86) || defined(_M_X64)
#define PLATFORM_X86 1
#endif
#else
#error "Unable to determine compiler"
#endif

/**
 * Users must call this macro to register their messages...
 *
 *  ...lest they be forced to type all sorts of boring and
 *  error-prone boiler plate code.
 *  blah blah blah... More specific documentation and explanation...
 *
 * @param MSG The type of message
 * @param TYPE The type of message
 *
 */
#define REGISTER_MESSAGE_TYPE(MSG, TYPE) \
    do_some(MSG, TYPE);                  \
    seriously();                         \
    crazy_stuff(MSG, TYPE);
