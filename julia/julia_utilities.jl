module WEB

    # Imports
    using HTTP, Sockets

    # Exports
    export get_page

    function download_page_data(url)
        #=
        This function will download data on the url page
        Return depends on response status and catched errors
        =#

        try
            # Get data
            response = HTTP.get(url)
            if typeof(response.status) <: Number && response.status == 200
                return String(response.body)
            end
        # Errors
        catch error
            if typeof(error) == Sockets.DNSError
                println(string("DNS error, please check your URL: ", url))
            end
        end
    end


end

module MATHS

    # Imports
    using LinearAlgebra

    # Exports
    export cosine_distance_float, cosine_distance_tensor

    function cosine_distance_float(x, y)
        #=
        Computhe the cosine distance between two vectors
        SLower than Distances.cosine_dist(x, y) but check more stuff about args
        =#
        if x isa Array && y isa Array
            if size(x) == size(y)
                cosine_distance = 1 - (dot(x,y) / (norm(x) * norm(y)))
                return cosine_distance
            else
                println("MATHS.cosine_distance_float: x and y do not have the same length.")
            end
        else
            println("MATHS.cosine_distance_float: x and/or y are not vectors.")
        end
    end

    function cosine_distance_tensor(x, y)

    end

end
