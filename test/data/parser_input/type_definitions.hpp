/// Not important.
struct type_definitions
{
    /// This is my bool.
    using my_bool = bool;

    /// This is really a string
    using really_a_string = std::string;

    /// This is a callback
    using callback = std::function<void(int times, int, uint8_t* data)>;
};
