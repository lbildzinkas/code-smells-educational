namespace OnlineStoreBadCode.DTOs;

public class AuthResponseDto
{
    public bool Success { get; set; }
    public string User { get; set; } = string.Empty;
    public int? UserId { get; set; }
    public string Message { get; set; } = string.Empty;
}