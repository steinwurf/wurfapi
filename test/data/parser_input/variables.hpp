/// Not important.
struct variables
{
    /// Special type for the variable a
    using my_type_const = bool;

    /// This is a a variable
    my_type_const a;

    /// This is a b variable
    const int b = 42;

    /// Test with alias
    constexpr static my_type_const eeee;

private:
    /// This is a c variable
    static mutable std::string c = "coool";

protected:
    /// This is a dddd variable
    constexpr static bool dddd = false;

    /// This is the size of dddd
    uint32_t size = sizeof(dddd);
};
