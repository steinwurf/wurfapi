/// Not important.
struct type_definitions
{
    /// This is my bool.
    using my_bool = bool;

    /// This is really a string
    using really_a_string = std::string;

    /// This is a callback
    using callback = std::function<void(int times, int, uint8_t* data)>;

    /// This is a c-style callback
    typedef void (*c_callback)(int times, int, uint8_t* data);

    /// This is an array tyoedef
    typedef int my_array[10];
};
