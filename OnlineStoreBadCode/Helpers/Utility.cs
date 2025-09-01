namespace OnlineStoreBadCode.Helpers;

// Code smell: Utility class with random unrelated methods
public static class Utility
{
    // Bad practice: method names that don't describe what they do
    public static object DoStuff(object input)
    {
        if (input == null)
        {
            return null;
        }
        
        // Bad practice: type checking with strings
        if (input.ToString().Contains("product"))
        {
            return "PROD_" + input.ToString().ToUpper();
        }
        else if (input.ToString().Contains("order"))
        {
            return "ORD_" + input.ToString().ToUpper();
        }
        else
        {
            return input;
        }
    }
    
    // Bad practice: method that does too many things
    public static string ProcessData(string data, int type, bool flag)
    {
        string result = "";
        
        // Bad practice: magic numbers
        if (type == 1)
        {
            result = data.ToUpper();
            if (flag)
            {
                result = result.Replace(" ", "_");
            }
        }
        else if (type == 2)
        {
            result = data.ToLower();
            if (flag)
            {
                result = result.Replace("_", " ");
            }
        }
        else if (type == 3)
        {
            // Bad practice: complex string manipulation
            for (int i = 0; i < data.Length; i++)
            {
                if (i % 2 == 0)
                {
                    result += data[i].ToString().ToUpper();
                }
                else
                {
                    result += data[i].ToString().ToLower();
                }
            }
        }
        else
        {
            // Bad practice: returning input when type is unknown
            result = data;
        }
        
        // Bad practice: side effect
        GlobalVariables.data = result;
        
        return result;
    }
    
    // Bad practice: method that should be in a Math class
    public static decimal CalculateSomething(decimal a, decimal b, string operation)
    {
        decimal result = 0;
        
        // Bad practice: string comparison for operations
        if (operation == "add")
        {
            result = a + b;
        }
        else if (operation == "subtract")
        {
            result = a - b;
        }
        else if (operation == "multiply")
        {
            result = a * b;
        }
        else if (operation == "divide")
        {
            // Bad practice: no zero check
            result = a / b;
        }
        else if (operation == "percentage")
        {
            result = (a / b) * 100;
        }
        else if (operation == "tax")
        {
            // Bad practice: hardcoded tax rate
            result = a * 1.15m;
        }
        
        // Bad practice: global state mutation
        GlobalVariables.x = (int)result;
        
        return result;
    }
    
    // Bad practice: SQL generation in utility class
    public static string BuildQuery(string table, Dictionary<string, object> conditions)
    {
        string sql = "SELECT * FROM " + table + " WHERE 1=1";
        
        // Bad practice: SQL injection vulnerability
        foreach (var kvp in conditions)
        {
            if (kvp.Value is string)
            {
                sql += $" AND {kvp.Key} = '{kvp.Value}'";
            }
            else if (kvp.Value is int || kvp.Value is decimal)
            {
                sql += $" AND {kvp.Key} = {kvp.Value}";
            }
            else if (kvp.Value is bool)
            {
                sql += $" AND {kvp.Key} = {((bool)kvp.Value ? 1 : 0)}";
            }
        }
        
        return sql;
    }
    
    // Bad practice: date manipulation with strings
    public static string FormatDate(DateTime date, int format)
    {
        switch (format)
        {
            case 1:
                return date.ToString("MM/dd/yyyy");
            case 2:
                return date.ToString("dd/MM/yyyy");
            case 3:
                return date.ToString("yyyy-MM-dd");
            case 4:
                return date.ToString("MMM dd, yyyy");
            case 5:
                // Bad practice: custom format
                return date.Day + " of " + date.ToString("MMMM") + ", " + date.Year;
            default:
                return date.ToString();
        }
    }
    
    // Bad practice: validation method that's too generic
    public static bool Validate(object value, string type)
    {
        try
        {
            if (type == "email")
            {
                // Bad practice: weak email validation
                return value.ToString().Contains("@");
            }
            else if (type == "phone")
            {
                // Bad practice: US-only phone validation
                return value.ToString().Length == 10;
            }
            else if (type == "creditcard")
            {
                // Bad practice: only checks length
                return value.ToString().Length == 16;
            }
            else if (type == "positive")
            {
                return Convert.ToDecimal(value) > 0;
            }
            else if (type == "notempty")
            {
                return !string.IsNullOrEmpty(value.ToString());
            }
            else
            {
                // Bad practice: default to true
                return true;
            }
        }
        catch
        {
            // Bad practice: swallow exceptions
            return false;
        }
    }
    
    // Bad practice: random number generator with side effects
    public static int GetRandomNumber(int min, int max)
    {
        Random rand = new Random(); // Bad practice: new Random each time
        int result = rand.Next(min, max);
        
        // Bad practice: logging in utility method
        GlobalVariables.errorMessages.Add($"Generated random number: {result}");
        
        return result;
    }
}