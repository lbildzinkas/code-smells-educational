using System.ComponentModel.DataAnnotations;

namespace OnlineStoreBadCode.DTOs;

public class LoginRequestDto
{
    [Required(ErrorMessage = "Email is required")]
    [EmailAddress(ErrorMessage = "Invalid email format")]
    public string Email { get; set; } = string.Empty;

    [Required(ErrorMessage = "Password is required")]
    [StringLength(100, MinimumLength = 3, ErrorMessage = "Password must be between 3 and 100 characters")]
    public string Password { get; set; } = string.Empty;
}