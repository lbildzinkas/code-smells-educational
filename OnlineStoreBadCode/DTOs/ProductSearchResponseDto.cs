namespace OnlineStoreBadCode.DTOs;

public class ProductSearchResponseDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public int Stock { get; set; }
    public bool LowStock { get; set; }
}