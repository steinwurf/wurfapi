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

/// A template class
/// @tparam T is a uint32_t
/// @tparam U is T
template <class T = uint32_t, typename U = T>
class another_type
{
public:
    /// With constructor
    another_type(const T& t);
};

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