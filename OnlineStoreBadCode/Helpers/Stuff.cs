namespace OnlineStoreBadCode.Helpers;

// Code smell: Poorly named class
public class Stuff
{
    // Bad practice: public fields instead of properties
    public string temp;
    public int counter;
    public object data;
    public bool flag;
    
    // Bad practice: constructor with side effects
    public Stuff()
    {
        counter = 0;
        flag = false;
        GlobalVariables.obj = this;
    }
    
    // Bad practice: method name gives no clue what it does
    public object Process(params object[] args)
    {
        // Bad practice: no parameter validation
        if (args.Length == 0)
        {
            return null;
        }
        
        // Bad practice: type checking with try-catch
        foreach (var arg in args)
        {
            try
            {
                int intVal = Convert.ToInt32(arg);
                counter += intVal;
            }
            catch
            {
                try
                {
                    string strVal = arg.ToString();
                    temp = temp + strVal;
                }
                catch
                {
                    data = arg;
                }
            }
        }
        
        // Bad practice: returning different types based on state
        if (counter > 0 && !string.IsNullOrEmpty(temp))
        {
            return new { number = counter, text = temp };
        }
        else if (counter > 0)
        {
            return counter;
        }
        else if (!string.IsNullOrEmpty(temp))
        {
            return temp;
        }
        else
        {
            return data;
        }
    }
    
    // Bad practice: method that changes behavior based on global state
    public string Transform(string input)
    {
        if (GlobalVariables.flag)
        {
            return input.ToUpper();
        }
        else if (GlobalVariables.x > 10)
        {
            return input.ToLower();
        }
        else if (GlobalVariables.isLoggedIn)
        {
            return "USER: " + input;
        }
        else
        {
            return input;
        }
    }
    
    // Bad practice: cache implementation without expiration
    private static Dictionary<string, object> cache = new Dictionary<string, object>();
    
    public object GetFromCache(string key)
    {
        if (cache.ContainsKey(key))
        {
            return cache[key];
        }
        
        // Bad practice: generating cache value in getter
        object value = null;
        if (key.StartsWith("product"))
        {
            value = "Cached Product Data";
        }
        else if (key.StartsWith("user"))
        {
            value = new { id = 1, name = "Cached User" };
        }
        else
        {
            value = DateTime.Now; // Bad practice: caching current time
        }
        
        cache[key] = value;
        return value;
    }
    
    // Bad practice: threading without synchronization
    public void DoAsync(Action action)
    {
        // Bad practice: fire and forget
        new System.Threading.Thread(() =>
        {
            try
            {
                action();
            }
            catch
            {
                // Bad practice: swallow all exceptions
            }
        }).Start();
    }
    
    // Bad practice: parsing method that modifies input
    public Dictionary<string, string> Parse(ref string input)
    {
        var result = new Dictionary<string, string>();
        
        // Bad practice: modifying ref parameter
        input = input.Trim().ToLower();
        
        // Bad practice: naive parsing
        var parts = input.Split('&');
        foreach (var part in parts)
        {
            var kvp = part.Split('=');
            if (kvp.Length == 2)
            {
                result[kvp[0]] = kvp[1];
            }
            else
            {
                // Bad practice: using index as key
                result[result.Count.ToString()] = part;
            }
        }
        
        // Bad practice: side effect
        this.data = result;
        
        return result;
    }
    
    // Bad practice: comparison method with side effects
    public bool Compare(object a, object b)
    {
        flag = false;
        
        try
        {
            // Bad practice: comparing everything as strings
            string strA = a.ToString();
            string strB = b.ToString();
            
            if (strA == strB)
            {
                flag = true;
                GlobalVariables.flag = true;
                return true;
            }
            
            // Bad practice: try numeric comparison
            try
            {
                double numA = Convert.ToDouble(a);
                double numB = Convert.ToDouble(b);
                
                // Bad practice: floating point equality
                if (numA == numB)
                {
                    flag = true;
                    return true;
                }
            }
            catch
            {
                // Continue with string comparison
            }
            
            // Bad practice: case-insensitive fallback
            if (strA.ToLower() == strB.ToLower())
            {
                flag = true;
                return true;
            }
            
            return false;
        }
        catch
        {
            // Bad practice: exception means equal?
            return true;
        }
    }
    
    // Bad practice: static and instance methods mixed
    public static void Reset()
    {
        cache.Clear();
        GlobalVariables.temp = null;
        GlobalVariables.data = null;
        GlobalVariables.obj = null;
        GlobalVariables.flag = false;
        GlobalVariables.x = 0;
    }
    
    // Bad practice: finalizer that does work
    ~Stuff()
    {
        // Bad practice: doing work in finalizer
        try
        {
            if (data != null)
            {
                GlobalVariables.temp = data.ToString();
            }
        }
        catch
        {
            // Ignore
        }
    }
}