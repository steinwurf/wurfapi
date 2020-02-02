
namespace project
{
inline namespace v1_0_0
{
namespace deprecated
{
/// @brief Different size coffee mugs
///
/// This lets you choose the size of your coffee mug
///
enum class mug_size
{
    /// The Short version
    Short = 8,
    /// The Tall version
    Tall,
    /// The Grande version
    /// Use it like so:
    ///
    ///     std::cout << mug_size::Grande << std::endl;
    Grande,
    /// @brief The Venti version 20 ounces.
    ///
    /// This one will keep you up
    /// all night!
    ///
    ///     std::cout << mug_size::Venti << std::endl;
    ///
    /// I hope you enjoy.
    Venti = 20
};
}
}
}