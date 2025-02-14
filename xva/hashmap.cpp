#include <vector>
#include <iostream>
#include <stdexcept>
#include <limits>
#include <memory>

template <typename KeyType, typename ValueType>
class HashMap
{
private:
    struct Node
    {
        KeyType key;
        ValueType value;
        bool _is_occupied;
    };
    std::size_t _capacity;
    std::size_t _usage;
    std::vector<Node> _map;

    void expand()
    {
        if (_capacity > std::numeric_limits<std::size_t>::max() / 2)
            throw std::logic_error("Capacity Reached");

        std::vector<Node> _old_map = _map;

        _capacity *= 2;
        _map.clear();
        _map.resize(_capacity);

        for (const auto &n : _old_map)
        {
            if (!n._is_occupied)
                continue;

            insert(n.key, n.value);

            _usage -= 1;
        }
    }

    std::size_t hash(const KeyType &key) const
    {
        return std::hash<KeyType>{}(key) % _capacity;
    }

public:
    HashMap(std::size_t capacity = 64)
    {
        _capacity = capacity;
        _usage = 0;

        _map = std::vector<Node>(_capacity);
    }

    void insert(const KeyType &key, const ValueType &value)
    {
        if ((_usage + 1.0) / _capacity > 0.5)
            expand();

        std::size_t index = hash(key);

        while (_map[index]._is_occupied)
            index = (index + 1) % _capacity;

        _map[index].key = key;
        _map[index].value = value;
        _map[index]._is_occupied = true;

        _usage += 1;
    }

    bool contains(const KeyType &key)
    {
        std::size_t index = hash(key);

        while (_map[index]._is_occupied)
        {
            if (_map[index].key == key)
                return true;

            index = (index + 1) % _capacity;
        }

        return false;
    }

    void remove(const KeyType &key)
    {
        std::size_t index = hash(key);

        while (_map[index]._is_occupied)
        {
            if (_map[index].key == key)
            {
                _map[index]._is_occupied = false;
                _usage -= 1;
                return;
            }

            index = (index + 1) % _capacity;
        }
    }

    std::size_t capacity()
    {
        return _capacity;
    }

    std::size_t usage()
    {
        return _usage;
    }
};

int main()
{
    std::unique_ptr<HashMap<char, int>> h(new HashMap<char, int>(4));

    h->insert('a', 10);
    h->insert('a', 11);
    h->insert('a', 12);
    h->remove('a');
    h->insert('a', 13);

    return 0;
}
