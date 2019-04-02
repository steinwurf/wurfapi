/// Not important.
struct variables
{
    /// Special type for the variable a
    using my_type_const = bool;

    /// This is a a variable
    my_type_const a;

    /// This is a b variable
    const int b = 42;

private:
    /// This is a c variable
    static mutable std::string c = "coool";

protected:
    /// This is a dddd variable
    constexpr static bool dddd = false;
};

