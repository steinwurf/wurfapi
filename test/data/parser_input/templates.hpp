/// A template class
///
/// @tparam T is a type
template <class T>
class our_type
{
public:
    /// With constructor
    our_type(const T& t);
};

/// Specialization
template <>
class our_type<int>
{
public:
    /// With int
    our_type(const int& t);
};

namespace test
{
/// A template class
/// @tparam T is a uint32_t
/// @tparam U is T
template <class T = uint32_t, typename U = T, typename... Args>
class another_type
{
public:
    /// With constructor
    another_type(const T& t);

    /// Nexted class
    template <class T>
    class nested
    {
        void print();
    };
};
}
/// Template template function
/// @tparam S something something...
/// @tparam H another something
template <template <class> class H, class S = our_type<int>>
void f(const H<S>& value)
{
}

/// A non-type template class
///
/// @tparam T is a type
template <uint32_t Value>
class non_type
{
public:
};

/// Template template struct
/// @tparam S something something...
/// @tparam H another something
template <template <class> class H, class S = our_type<int>>
struct testtest
{
};

/// Test overload on number of template args - unique name should be
/// different
template <class A>
void test();

template <class A, class B>
void test();

/// Specilization
template <typename R, typename... Args>
class function<R(Args...)>
{
};